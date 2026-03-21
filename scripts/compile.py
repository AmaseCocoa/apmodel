import hashlib
import json
import logging
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

import niquests
import yaml
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from jinja2 import Environment, FileSystemLoader

SNAKE_RE = re.compile(r"(?<!^)(?=[A-Z])")
ruff_path = shutil.which("ruff")

logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")
logger = logging.getLogger(__name__)

AS2_NS = "https://www.w3.org/ns/activitystreams#"
VENDOR_TYPE_MAPPING_PATH = Path("_vendor") / "type_mapping.py"


def get_hash(*strings: str) -> str:
    return hashlib.sha256("".join(strings).encode()).hexdigest()


def to_snake(name: str) -> str:
    return SNAKE_RE.sub("_", name).lower()


def mixin_to_file(name: str) -> str:
    return to_snake(name).replace("_mixin", "")


def to_python_type(type_str: str) -> str:
    if not type_str:
        return "Any"
    if "|" not in type_str and "Optional" not in type_str and type_str not in ["Any", "None"]:
        well_known = {
            "str",
            "int",
            "float",
            "bool",
            "dict",
            "list",
            "datetime.datetime",
            "datetime",
        }
        if type_str not in well_known:
            return f"'{type_str}'"
    return type_str


def generate_as2_type_registry(as2_schema: Path | None = None) -> dict:
    url = "https://www.w3.org/ns/activitystreams"
    headers = {"Accept": "application/ld+json"}
    try:
        if not as2_schema or not as2_schema.exists():
            res = niquests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            data = res.json()
        else:
            with open(as2_schema) as f:
                data = json.load(f)["schema"]
        context = data.get("@context", {})
    except Exception as e:  # noqa: BLE001
        logger.warning(f"Failed to fetch AS2 context: {e}")
        return {}

    as2_classes = {k for k in context if k and k[0].isupper()}
    registry = {}
    PROPERTY_HINTS = {
        "url": "Link | str",
        "icon": "Link | str",
        "image": "Link | str",
        "href": "str",
        "preview": "Object | Link | str",
        "actor": "Object | str",
        "object": "Object | str",
        "target": "Object | str",
        "inbox": "str",
        "outbox": "str",
        "followers": "str",
        "following": "str",
        "liked": "str",
        "likes": "str",
        "shares": "str",
    }
    XSD_TO_PY = {
        "xsd:dateTime": "datetime",
        "xsd:nonNegativeInteger": "int",
        "xsd:integer": "int",
        "xsd:float": "float",
        "xsd:boolean": "bool",
    }

    for key, val in context.items():
        if key and key[0].islower():
            if isinstance(val, dict):
                if val.get("@container") == "@language":
                    py_type = "Dict[str, str]"
                else:
                    ld_type = val.get("@type", "@id")
                    base_ld_type = ld_type.split(":")[-1]
                    if key in PROPERTY_HINTS:
                        base = PROPERTY_HINTS[key]
                    elif ld_type in XSD_TO_PY:
                        base = XSD_TO_PY[ld_type]
                    elif base_ld_type in as2_classes:
                        base = base_ld_type
                    elif ld_type == "@id":
                        base = "Object | str"
                    else:
                        base = "str"
                    py_type = f"{base} | List[{base}] | None"
            elif isinstance(val, str):
                py_type = "str | None"
            else:
                continue
            registry[key] = py_type
    return registry


def generate_type_mapping(
    schema_root: str,
    output_root: str,
    cache_dir: str | None = None,
) -> None:
    output_path = Path(output_root)
    schema_path = Path(schema_root)
    cache_path = Path(cache_dir) if cache_dir else Path(".cache") / "schema_compile"

    mappings: dict[str, str] = {}
    yaml_hashes = ""

    for yaml_file in sorted(schema_path.rglob("*.yaml")):
        yaml_raw = yaml_file.read_text()
        yaml_hashes += yaml_raw

        rel_path = yaml_file.relative_to(schema_path)
        config = yaml.safe_load(yaml_raw)
        classes_config = config.get("classes", {})

        for class_name, c in classes_config.items():
            if c.get("isCoreType"):
                continue

            as2_uri = c.get("as2Uri")
            uri = as2_uri or f"{AS2_NS}{class_name}"

            parts = list(rel_path.parent.parts) + [rel_path.stem]
            module_path = ".".join(parts)
            dotted = f"apmodel.{module_path}.{class_name}"
            mappings[uri] = dotted

    current_hash = get_hash(yaml_hashes)
    hash_file = cache_path / (str(VENDOR_TYPE_MAPPING_PATH) + ".hash")
    target_file = output_path / VENDOR_TYPE_MAPPING_PATH

    if hash_file.exists() and target_file.exists() and hash_file.read_text() == current_hash:
        return

    lines = ["from __future__ import annotations", "", "TYPE_MAPPING: dict[str, str] = {"]
    for uri, dotted in sorted(mappings.items()):
        lines.append(f'    "{uri}": "{dotted}",')
    lines.append("}")
    lines.append("")

    content = "\n".join(lines)
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text(content, encoding="utf-8")

    hash_file.parent.mkdir(parents=True, exist_ok=True)
    hash_file.write_text(current_hash, encoding="utf-8")
    logger.info(f"--> Generated: {target_file}")

    if ruff_path:
        try:
            subprocess.run(  # noqa: S603
                [ruff_path, "format", str(target_file)],
                capture_output=True,
                text=True,
                check=True,
                shell=False,
                cwd=os.getcwd(),
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"Ruff format failed: {e.stderr}")


def generate_all(
    schema_root: str,
    output_root: str,
    template_dir: str,
    cache_dir: str | None = None,
    build_data: dict[str, list] | None = None,
):
    output_path = Path(output_root)
    schema_path = Path(schema_root)

    # キャッシュディレクトリの設定
    cache_path = Path(cache_dir) if cache_dir else Path(".cache/schema_compile")
    cache_path.mkdir(parents=True, exist_ok=True)

    as2_registry = generate_as2_type_registry(
        output_path / "_vendor" / "tinyjld" / "schema" / "as2.jsonld"
    )

    env = Environment(
        loader=FileSystemLoader(template_dir),
        extensions=["jinja2.ext.do"],
        autoescape=False,  # noqa: S701
    )
    env.filters["to_snake"] = to_snake
    env.filters["mixin_to_file"] = mixin_to_file
    env.filters["to_python_type"] = to_python_type

    template = env.get_template("model.j2")
    template_content = (Path(template_dir) / "model.j2").read_text()

    changed_files: list[str] = []

    for yaml_file in schema_path.rglob("*.yaml"):
        yaml_raw = yaml_file.read_text()
        current_hash = get_hash(yaml_raw, template_content)

        rel_path = yaml_file.relative_to(schema_path)
        target_file = output_path / rel_path.parent / f"{yaml_file.stem}.py"

        hash_file = cache_path / rel_path.with_suffix(".hash")

        if hash_file.exists() and target_file.exists() and hash_file.read_text() == current_hash:
            if build_data:
                build_data["artifacts"].append(os.path.relpath(str(target_file), os.getcwd()))
            continue

        config = yaml.safe_load(yaml_raw)
        dot_prefix = "." * (len(rel_path.parent.parts) + 1)
        classes_config = config.get("classes", {})
        current_mixins = set()

        for c_name, c in classes_config.items():
            current_mixins.update(c.get("mixins") or [])
            properties = c.get("properties") or {}
            for p_name, p_conf in properties.items():
                if p_conf is None:
                    properties[p_name] = p_conf = {}
                p_conf["type"] = to_python_type(
                    p_conf.get("type") or as2_registry.get(p_name, "Any")
                )

                field_args = ["kw_only=True"]
                if p_conf.get("alias"):
                    field_args.append(f"alias='{p_conf['alias']}'")

                if "default" in p_conf:
                    field_args.append(f"default={p_conf['default']}")
                elif "default_factory" in p_conf:
                    field_args.append(f"default_factory={p_conf['default_factory']}")
                elif p_name == "type":
                    field_args.append(f"default='{c_name}'")
                elif "None" in p_conf["type"] or "Optional" in p_conf["type"]:
                    field_args.append("default=None")
                elif "list[" in p_conf["type"].lower():
                    field_args.append("default_factory=list")
                elif "dict[" in p_conf["type"].lower():
                    field_args.append("default_factory=dict")

                p_conf["_rendered_field"] = f"Field({', '.join(field_args)})"

        rendered = template.render(
            classes=classes_config,
            dot_prefix=dot_prefix,
            mixins=sorted(list(current_mixins)),
            external_imports=config.get("imports", []),
        )

        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(rendered, encoding="utf-8")

        hash_file.parent.mkdir(parents=True, exist_ok=True)
        hash_file.write_text(current_hash, encoding="utf-8")

        changed_files.append(str(target_file))
        logger.info(f"--> Compiled: {target_file}")

        if build_data:
            build_data["artifacts"].append(os.path.relpath(str(target_file), os.getcwd()))

    if ruff_path and changed_files:
        logger.info(f"--> Formatting with Ruff ({ruff_path})...")
        try:
            ruff_rules = ["I", "UP", "B", "F401", "TC005"]
            project_root = os.getcwd()
            a = [
                ruff_path,
                "check",
                "--select",
                ",".join(ruff_rules),
                "--fix",
                *changed_files,
            ]
            a2 = [ruff_path, "format", *changed_files]
            subprocess.run(  # noqa: S603 # using fixed and internal variable
                a,
                capture_output=True,
                text=True,
                check=True,
                shell=False,
                cwd=project_root,
            )
            subprocess.run(  # noqa: S603 # same as L244
                a2,
                capture_output=True,
                text=True,
                check=True,
                shell=False,
                cwd=project_root,
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"Ruff failed (exit {e.returncode}):\n{e.stderr}\n{e.stdout}")

    generate_type_mapping(
        schema_root,
        output_root,
        cache_dir=cache_dir,
    )


class SchemaCompilerHook(BuildHookInterface):
    def initialize(self, version: str, build_data: dict[str, Any]):
        root = Path(self.root)
        generate_all(
            str(root / "schemas"),
            str(root / "src" / "apmodel"),
            str(root / "templates"),
            cache_dir=str(root / ".cache" / "schema_compile"),
            build_data=build_data,
        )


if __name__ == "__main__":
    generate_all("schemas", "src/apmodel", "templates", ".cache/schema_compile")
