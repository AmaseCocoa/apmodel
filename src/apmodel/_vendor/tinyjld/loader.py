import glob
import ipaddress
import json
import logging
import os
import socket
import threading
from typing import Any
from urllib.parse import urlparse

import niquests

logger = logging.getLogger("tinyjld.loader")
DEFAULT_PRELOADS_DIR = os.path.join(os.path.dirname(__file__), "schema")


class TinyJLDLoader:
    __slots__ = (
        "timeout",
        "preloads_dir",
        "preload_mappings",
        "path_to_mappings",
        "session",
        "__lock",
    )

    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.preloads_dir = DEFAULT_PRELOADS_DIR
        self.preload_mappings: dict[str, dict] = {}
        self.path_to_mappings: dict[str, str] = {}

        self.session = niquests.Session()
        self.session.headers.update(
            {
                "Accept": 'application/ld+json;profile="http://www.w3.org/ns/json-ld#context", application/ld+json, application/json;q=0.5'
            }
        )

        self.__lock = threading.Lock()

        if DEFAULT_PRELOADS_DIR and os.path.isdir(DEFAULT_PRELOADS_DIR):
            self._scan_preloads(DEFAULT_PRELOADS_DIR)

    def _scan_preloads(self, directory: str):
        for path in glob.glob(os.path.join(directory, "*.jsonld")):
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
                    urls = data.get("urls")
                    if isinstance(urls, list):
                        with self.__lock:
                            for url in urls:
                                self.path_to_mappings[url] = path
            except (OSError, json.JSONDecodeError) as e:
                logger.warning(f"Failed to scan preload {path}: {e}")

    def _read_schema(self, path: str) -> dict[str, Any]:
        if schema := self.preload_mappings.get(path):
            return schema

        with self.__lock:
            if schema := self.preload_mappings.get(path):
                return schema
            try:
                with open(path, encoding="utf-8") as f:
                    schema = json.load(f).get("schema", {})
                    if not self.preload_mappings.get(path):
                        self.preload_mappings[path] = schema
                    return schema
            except (OSError, json.JSONDecodeError):
                return {}

    def is_safe_url(self, url: str) -> bool:
        parsed = urlparse(url)
        if not parsed.hostname:
            return False
        default_port = 80 if parsed.scheme == "http" else 443
        port = parsed.port or default_port
        try:
            infos = socket.getaddrinfo(
                parsed.hostname,
                port,
            )
            for info in infos:
                ip_str = info[4][0]
                ip = ipaddress.ip_address(ip_str)
                if ip.is_private or ip.is_loopback:
                    return False
            return True
        except (socket.gaierror, ValueError):
            return False

    def __call__(self, url: str) -> dict[str, Any]:
        if url in self.path_to_mappings:
            return self._read_schema(self.path_to_mappings[url])

        parsed = urlparse(url)
        if parsed.path.endswith(
            (
                "/contexts/litepub.jsonld",
                "/litepub.jsonld",
                "/schemas/litepub-0.1.jsonld",
            )
        ):
            lp_path = (
                os.path.join(self.preloads_dir, "litepub-0.1.jsonld")
                if self.preloads_dir
                else None
            )
            if lp_path and os.path.exists(lp_path):
                return self._read_schema(lp_path)

        if not self.is_safe_url(url):
            logger.error(f"Blocked private network access: {url}")
            return {}

        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            content_type = response.headers.get("Content-Type", "")
            if (
                not isinstance(content_type, str)
                or "json" not in content_type.lower()
            ):
                logger.warning(
                    f"Skipping non-JSON response ({content_type}) from {url}"
                )
                return {}

            return response.json()
        except niquests.RequestException as e:
            logger.debug(f"Fetch failed: {url} -> {e}")
            return {}
        except json.JSONDecodeError:
            logger.debug(f"Invalid JSON from: {url}")
            return {}
