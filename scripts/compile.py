import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

import niquests
import yaml
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from jinja2 import Environment, FileSystemLoader


def generate_as2_type_registry():
    url = "https://www.w3.org/ns/activitystreams"
    headers = {"Accept": "application/ld+json"}

    try:
        res = niquests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        context = res.json().get("@context", {})
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
    well_known = {
        "str",
        "int",
        "float",
        "bool",
        "Any",
        "None",
        "dict",
        "list",
        "datetime.datetime",
        "datetime",
    }
    if not type_str:
        return "Any"
    if "|" in type_str or "[" in type_str:
        return type_str
    if type_str in well_known:
        return type_str
    return f"'{type_str}'"


def generate_all(schema_root: str, output_root: str, template_dir: str, build_data: Optional[Dict[str, List]] = None):
    as2_registry = generate_as2_type_registry()

    env = Environment(
        loader=FileSystemLoader(template_dir), extensions=["jinja2.ext.do"]
    )
    env.filters["to_snake"] = to_snake
    env.filters["mixin_to_file"] = mixin_to_file
    env.filters["to_python_type"] = to_python_type

    template = env.get_template("model-new.py.j2")

    schema_path = Path(schema_root)
    output_path = Path(output_root)

    for yaml_file in schema_path.rglob("*.yaml"):
        with open(yaml_file, "r") as f:
            config = yaml.safe_load(f)

        rel_to_root = yaml_file.relative_to(schema_path).parent
        depth = len(rel_to_root.parts)
        dot_prefix = "." * (depth + 1)

        current_mixins = set()
        classes_config = config.get("classes", {})
        for c_name, c in classes_config.items():
            mixins = c.get("mixins") or []
            current_mixins.update(mixins)

            properties = c.get("properties") or {}
            for p_name, p_conf in properties.items():
                if p_conf is None:
                    properties[p_name] = p_conf = {}

                if not p_conf.get("type"):
                    p_conf["type"] = as2_registry.get(p_name, "Any")

                if "default" not in p_conf and "default_factory" not in p_conf:
                    prop_type = p_conf["type"]
                    if p_name == "type":
                        p_conf["default"] = f'"{c_name}"'
                    elif "None" in prop_type or "Optional" in prop_type:
                        p_conf["default"] = "None"
                    elif (
                        "List[" in prop_type
                        or "list[" in prop_type
                        or prop_type.endswith("[]")
                    ):
                        p_conf["default_factory"] = "list"
                    elif "Dict[" in prop_type or "dict[" in prop_type:
                        p_conf["default_factory"] = "dict"
                    else:
                        p_conf["default"] = "None"

        target_file = output_path / rel_to_root / f"{yaml_file.stem}.py"
        target_file.parent.mkdir(parents=True, exist_ok=True)

        rendered = template.render(
            classes=classes_config,
            dot_prefix=dot_prefix,
            mixins=sorted(list(current_mixins)),
            external_imports=config.get("imports", []),
        )

        with open(target_file, "w") as f:
            f.write(rendered)

        with open(os.devnull, "w") as fnull:
            subprocess.run(
                ["ruff", "format", str(target_file)],
                check=True,
                stdout=fnull,
                stderr=fnull,
            )
            subprocess.run(
                [
                    "ruff",
                    "check",
                    "--select",
                    "I,F401",
                    "--fix",
                    str(target_file),
                ],
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

        generate_all(str(schemas), str(src_apmodel), str(templates), build_data=build_data)


if __name__ == "__main__":
    generate_all("schemas", "src/apmodel", "templates")
