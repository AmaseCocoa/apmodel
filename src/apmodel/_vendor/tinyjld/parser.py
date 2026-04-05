# SPDX-License-Identifier: MIT
# Copyright (c) 2026 AmaseCocoa
# Smallest JSON-LD parser made for apmodel

import threading
from collections.abc import Callable
from typing import Any


class TinyJLD:
    __slots__ = ("loader", "__context_cache", "__lock")

    def __init__(self, loader: Callable[[str], dict[str, Any]]):
        self.loader = loader
        self.__context_cache = {}
        self.__lock = threading.RLock()

    def fetch_remote_context(self, url: str) -> dict[str, Any]:
        if url in self.__context_cache:
            return self.__context_cache[url]

        with self.__lock:
            if url in self.__context_cache:
                return self.__context_cache[url]
            try:
                data = self.loader(url)
                ctx = (
                    data.get("@context", data) if isinstance(data, dict) else {}
                )
                res = self.flatten_context(ctx)
                self.__context_cache[url] = res
                return res
            except (OSError, RuntimeError, ValueError):
                self.__context_cache[url] = {}
                return {}

    def flatten_context(
        self, ctx_input: str | dict | list | None
    ) -> dict[str, Any]:
        if not ctx_input:
            return {}
        if isinstance(ctx_input, dict):
            return ctx_input

        merged = {}
        items = ctx_input if isinstance(ctx_input, list) else [ctx_input]
        for item in items:
            if isinstance(item, str):
                merged.update(self.fetch_remote_context(item))
            elif isinstance(item, dict):
                merged.update(item)
        return merged

    def expand_term(
        self,
        term: object,
        context: dict[str, Any],
        seen: set[str] | None = None,
    ) -> object:
        if not isinstance(term, str) or term.startswith("@"):
            return term

        if ":" in term:
            prefix, suffix = term.split(":", 1)
            if suffix.startswith("//"):
                return term
            if prefix in context:
                if seen is None:
                    seen = set()
                if term in seen:
                    return term
                seen.add(term)
                base = context[prefix]
                base_iri = base.get("@id") if isinstance(base, dict) else base
                if isinstance(base_iri, str):
                    return (
                        f"{self.expand_term(base_iri, context, seen)}{suffix}"
                    )

        if term in context:
            mapping = context[term]
            val = mapping.get("@id") if isinstance(mapping, dict) else mapping
            if isinstance(val, str) and val != term:
                if seen is None:
                    seen = set()
                if term in seen:
                    return term
                seen.add(term)
                return self.expand_term(val, context, seen)
            return val

        vocab = context.get("@vocab")
        return f"{vocab}{term}" if vocab and isinstance(vocab, str) else term

    def resolve(
        self,
        data: dict[str, Any],
        parent_context: dict[str, Any] | None = None,
    ) -> str | None:
        if not isinstance(data, dict):
            return None

        ctx: dict[str, Any] = {}

        # First, inherit parent context if provided
        if parent_context and isinstance(parent_context, dict):
            # If parent_context has @context, use it
            if "@context" in parent_context:
                ctx.update(self.flatten_context(parent_context["@context"]))
            # Otherwise, parent_context itself is the flattened context
            else:
                ctx.update(parent_context)

        # Then add/update with the data's own @context
        if "@context" in data:
            ctx.update(self.flatten_context(data["@context"]))

        raw_type = data.get("@type") or data.get("type")
        if not raw_type:
            return None

        target = (
            raw_type[0] if isinstance(raw_type, list) and raw_type else raw_type
        )
        res = self.expand_term(target, ctx)
        return str(res) if res else None
