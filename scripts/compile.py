import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

import niquests
import yaml
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from jinja2 import Environment, FileSystemLoader


def get_hash(*strings: str) -> str:
    return hashlib.md5("".join(strings).encode()).hexdigest()


def generate_as2_type_registry(as2_schema: Optional[Path] = None):
    url = "https://www.w3.org/ns/activitystreams"
    headers = {"Accept": "application/ld+json"}

    try:
        if not as2_schema:
            res = niquests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            data = res.json()
        else:
            with open(as2_schema, "r") as f:
                data = json.load(f)["schema"]
        context = data.get("@context", {})
    except Exception as e:
        print(f"Warning: Failed to fetch AS2 context: {e}")
        return {}

    XSD_TO_PY = {
        "xsd:dateTime": "datetime.datetime",
        "xsd:nonNegativeInteger": "int",
        "xsd:integer": "int",
        "xsd:float": "float",
        "xsd:boolean": "bool",
    }

    as2_classes = {k for k in context.keys() if k and k[0].isupper()}

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
                if val == "@id":
                    py_type = "str | None"
                else:
                    py_type = "str | None"
            else:
                continue

            registry[key] = py_type

    return registry


def to_snake(name: str) -> str:
    import re

    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def mixin_to_file(name: str) -> str:
    return to_snake(name).replace("_mixin", "")


def to_python_type(type_str: str) -> str:
    if not type_str:
        return "Any"

    if "|" not in type_str and "Optional" not in type_str:
        if type_str not in ["Any", "None"]:
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


def generate_all(
    schema_root: str,
    output_root: str,
    template_dir: str,
    build_data: Optional[Dict[str, List]] = None,
):
    as2_registry = generate_as2_type_registry(
        Path(output_root) / "_vendor" / "tinyjld" / "schema" / "as2.jsonld"
    )

    env = Environment(
        loader=FileSystemLoader(template_dir), extensions=["jinja2.ext.do"]
    )
    env.filters["to_snake"] = to_snake
    env.filters["mixin_to_file"] = mixin_to_file
    env.filters["to_python_type"] = to_python_type

    template = env.get_template("model.j2")
    template_path = Path(template_dir) / "model.j2"
    template_content = template_path.read_text()

    schema_path = Path(schema_root)
    output_path = Path(output_root)

    for yaml_file in schema_path.rglob("*.yaml"):
        yaml_raw = yaml_file.read_text()
        current_hash = get_hash(yaml_raw, template_content)
        config = yaml.safe_load(yaml_raw)

        rel_to_root = yaml_file.relative_to(schema_path).parent
        target_file = output_path / rel_to_root / f"{yaml_file.stem}.py"
        hash_file = target_file.with_suffix(".py.hash")
        
        if hash_file.exists() and hash_file.read_text() == current_hash and target_file.exists():
            if build_data:
                build_data["artifacts"].append(os.path.relpath(str(target_file), os.getcwd()))
            continue
            
        dot_prefix = "." * (len(rel_to_root.parts) + 1)
        current_mixins = set()
        classes_config = config.get("classes", {})

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
                    field_args.append(
                        f"default_factory={p_conf['default_factory']}"
                    )
                elif p_name == "type":
                    field_args.append(f"default='{c_name}'")
                elif any(
                    x in p_conf["type"] for x in ["None", "Optional", "|"]
                ):
                    field_args.append("default=None")
                elif "list[" in p_conf["type"].lower():
                    field_args.append("default_factory=list")
                elif "dict[" in p_conf["type"].lower():
                    field_args.append("default_factory=dict")
                else:
                    field_args.append("default=None")

                p_conf["_rendered_field"] = f"Field({', '.join(field_args)})"

        target_file = output_path / rel_to_root / f"{yaml_file.stem}.py"
        rendered = template.render(
            classes=classes_config,
            dot_prefix=dot_prefix,
            mixins=sorted(list(current_mixins)),
            external_imports=config.get("imports", []),
        )

        if target_file.exists():
            with open(target_file, "r", encoding="utf-8") as f:
                if f.read() == rendered:
                    print(f"--> Skipped (No change): {target_file}")
                    if build_data:
                        build_data["artifacts"].append(
                            os.path.relpath(str(target_file), os.getcwd())
                        )
                    continue

        target_file.parent.mkdir(parents=True, exist_ok=True)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(rendered)

        with open(os.devnull, "w") as fnull:
            subprocess.run(
                [
                    "ruff",
                    "check",
                    "--select",
                    "I,UP,B,F401",
                    "--fix",
                    str(target_file),
                ],
                check=True,
                stdout=fnull,
                stderr=fnull,
            )
            subprocess.run(
                ["ruff", "format", str(target_file)],
                check=True,
                stdout=fnull,
                stderr=fnull,
            )

        print(f"--> Compiled: {target_file}")
        if build_data:
            relative_path = os.path.relpath(str(target_file), os.getcwd())
            build_data["artifacts"].append(relative_path)


class SchemaCompilerHook(BuildHookInterface):
    def initialize(self, version, build_data):
        script_path = Path(self.root) / "scripts" / "compile.py"
        schemas = Path(self.root) / "schemas"
        templates = Path(self.root) / "templates"
        src_apmodel = Path(self.root) / "src" / "apmodel"

        print(f"--> Compiling Schema: {script_path}")

        generate_all(
            str(schemas),
            str(src_apmodel),
            str(templates),
            build_data=build_data,
        )


if __name__ == "__main__":
    generate_all("schemas", "src/apmodel", "templates")
