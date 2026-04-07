import hashlib
import json
import logging
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import niquests
import yaml
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from jinja2 import Environment, FileSystemLoader

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib  # ty: ignore[unresolved-import]

SNAKE_RE = re.compile(r"(?<!^)(?=[A-Z])")
ruff_path = shutil.which("ruff")
if not ruff_path:
    import subprocess

    result = subprocess.run(
        ["uv", "run", "--quiet", "ruff", "--version"],  # noqa: S607
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        ruff_path = "uv"

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
            "NonNegativeInt",
            "PositiveInt",
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

    lines = ["from __future__ import annotations", "", "TYPE_MAPPING: dict[str, tuple[str, str]] = {"]
    for uri, dotted in sorted(mappings.items()):
        lines.append(f'    "{uri}": ("{dotted}", "apmodel"),')
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
            base_cmd = [ruff_path, "run", "ruff"] if ruff_path == "uv" else [ruff_path]
            subprocess.run(  # noqa: S603
                base_cmd + ["format", str(target_file)],
                capture_output=True,
                text=True,
                check=True,
                shell=False,
                cwd=os.getcwd(),
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"Ruff format failed: {e.stderr}")


def generate_init_files(output_root: str, template_dir: str) -> list[str]:
    output_path = Path(output_root)
    changed_files: list[str] = []
    cache_path = Path(".cache") / "init_files"
    cache_path.mkdir(parents=True, exist_ok=True)

    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=False, # noqa: S701
    )

    root_init = output_path / "__init__.py"
    template = env.get_template("init.j2")

    all_classes: dict[str, list[str]] = {}

    for py_file in output_path.rglob("*.py"):
        if py_file.name == "__init__.py" or py_file.name.startswith("_"):
            continue
        content = py_file.read_text(encoding="utf-8")
        class_names = re.findall(r"^class\s+(\w+)\s*[:(]", content, re.MULTILINE)
        if not class_names:
            continue
        parent = py_file.parent
        rel_path = parent.relative_to(output_path)
        module_name = py_file.stem if parent == output_path else str(rel_path).replace("/", ".")
        if module_name not in all_classes:
            all_classes[module_name] = []
        all_classes[module_name].extend(sorted(set(class_names)))

    new_content = template.render(modules=all_classes)

    hash_file = cache_path / "root_init.hash"
    current_hash = get_hash(new_content)

    needs_update = True
    if hash_file.exists() and root_init.exists() and hash_file.read_text() == current_hash:
        needs_update = False

    if needs_update:
        root_init.write_text(new_content, encoding="utf-8")
        hash_file.parent.mkdir(parents=True, exist_ok=True)
        hash_file.write_text(current_hash, encoding="utf-8")
        changed_files.append(str(root_init))
        logger.info(f"--> Created: {root_init}")

    subdirs: dict[Path, list[str]] = {}
    for py_file in output_path.rglob("*.py"):
        if py_file.name == "__init__.py" or py_file.name.startswith("_"):
            continue
        parent = py_file.parent
        if parent == output_path:
            continue
        if parent not in subdirs:
            subdirs[parent] = []
        content = py_file.read_text(encoding="utf-8")
        if "# compiler: skip" in content:
            continue
            
        class_names = re.findall(r"^class\s+(\w+)\s*[:(]", content, re.MULTILINE)
        subdirs[parent].extend(class_names)

    for parent_dir, class_names in subdirs.items():
        init_file = parent_dir / "__init__.py"
        sorted_classes = sorted(set(class_names))

        unique_imports = []
        seen = set()
        for py_file in sorted(parent_dir.glob("*.py")):
            if py_file.name == "__init__.py" or py_file.name.startswith("_"):
                continue
            content = py_file.read_text(encoding="utf-8")
            class_names_in_file = re.findall(r"^class\s+(\w+)\s*[:(]", content, re.MULTILINE)
            for cls in sorted(class_names_in_file):
                line = f"from .{py_file.stem} import {cls}"
                if line not in seen:
                    seen.add(line)
                    unique_imports.append(line)

        sub_content = "from __future__ import annotations\n\n" + "\n".join(unique_imports) + "\n\n__all__ = [" + ", ".join(f'"{c}"' for c in sorted_classes) + "]\n"

        sub_hash_file = cache_path / f"sub_{str(parent_dir.relative_to(output_path)).replace('/', '_')}.hash"
        sub_hash = get_hash(sub_content)

        sub_needs_update = True
        if init_file.exists():
            current_content = init_file.read_text(encoding="utf-8")
            if "# compiler: skip" in current_content:
                continue
            
            if sub_hash_file.exists() and sub_hash_file.read_text() == sub_hash:
                sub_needs_update = False
        

        if sub_needs_update:
            init_file.write_text(sub_content, encoding="utf-8")
            sub_hash_file.parent.mkdir(parents=True, exist_ok=True)
            sub_hash_file.write_text(sub_hash, encoding="utf-8")
            changed_files.append(str(init_file))
            logger.info(f"--> Created: {init_file}")

    return changed_files


def generate_all(
    schema_root: str,
    output_root: str,
    template_dir: str,
    cache_dir: str | None = None,
    build_data: dict[str, list] | None = None,
):
    output_path = Path(output_root)
    schema_path = Path(schema_root)

    cache_path = Path(cache_dir) if cache_dir else Path(".cache/schema_compile")
    cache_path.mkdir(parents=True, exist_ok=True)

    as2_registry = generate_as2_type_registry(output_path / "_vendor" / "tinyjld" / "schema" / "as2.jsonld")

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
                p_conf["type"] = to_python_type(p_conf.get("type") or as2_registry.get(p_name, "Any"))
                additional_args = p_conf.get("additionalFieldArgs")

                field_args = ["kw_only=True"]
                if p_conf.get("alias"):
                    field_args.append(f"alias='{p_conf['alias']}'")
                if additional_args:
                    for arg_name, arg_val in additional_args.items():
                        field_args.append(f"{arg_name}={arg_val}")

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
            project_root = os.getcwd()
            pyproject = Path(project_root) / "pyproject.toml"
            ruff_select = None
            ruff_ignore = None
            if pyproject.exists():
                with open(pyproject, "rb") as f:
                    pyproject_data = tomllib.load(f)
                ruff_config = pyproject_data.get("tool", {}).get("ruff", {})
            ruff_select = ruff_config.get("lint", {}).get("select")
            ruff_ignore = ruff_config.get("lint", {}).get("ignore")
            base_cmd = [ruff_path, "run", "ruff"] if ruff_path == "uv" else [ruff_path]
            a = base_cmd + ["check", "--fix", *changed_files]
            if ruff_select:
                a.extend(["--select", ",".join(ruff_select)])
            if ruff_ignore:
                a.extend(["--ignore", ",".join(ruff_ignore)])
            a2 = base_cmd + ["format", *changed_files]
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

    init_changed_files = generate_init_files(output_root, template_dir)
    changed_files.extend(init_changed_files)


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