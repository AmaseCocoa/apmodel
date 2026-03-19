import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

import niquests
import yaml
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from jinja2 import Environment, FileSystemLoader

# 正規表現を事前にコンパイル
SNAKE_RE = re.compile(r"(?<!^)(?=[A-Z])")

def get_hash(*strings: str) -> str:
    return hashlib.md5("".join(strings).encode()).hexdigest()

def to_snake(name: str) -> str:
    return SNAKE_RE.sub("_", name).lower()

def mixin_to_file(name: str) -> str:
    return to_snake(name).replace("_mixin", "")

def to_python_type(type_str: str) -> str:
    if not type_str:
        return "Any"
    if "|" not in type_str and "Optional" not in type_str:
        if type_str not in ["Any", "None"]:
            well_known = {
                "str", "int", "float", "bool", "dict", "list",
                "datetime.datetime", "datetime",
            }
            if type_str not in well_known:
                return f"'{type_str}'"
    return type_str

def generate_as2_type_registry(as2_schema: Path | None = None):
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
    except Exception as e:
        print(f"Warning: Failed to fetch AS2 context: {e}")
        return {}

    as2_classes = {k for k in context.keys() if k and k[0].isupper()}
    registry = {}
    PROPERTY_HINTS = {
        "url": "Link | str", "icon": "Link | str", "image": "Link | str",
        "href": "str", "preview": "Object | Link | str", "actor": "Object | str",
        "object": "Object | str", "target": "Object | str", "inbox": "str",
        "outbox": "str", "followers": "str", "following": "str",
        "liked": "str", "likes": "str", "shares": "str",
    }
    XSD_TO_PY = {
        "xsd:dateTime": "datetime.datetime", "xsd:nonNegativeInteger": "int",
        "xsd:integer": "int", "xsd:float": "float", "xsd:boolean": "bool",
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

    env = Environment(loader=FileSystemLoader(template_dir), extensions=["jinja2.ext.do"])
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
        
        # ハッシュファイルを .cache 内に配置 (平坦化を避けるため相対構造を維持)
        hash_file = cache_path / rel_path.with_suffix(".hash")
        
        if hash_file.exists() and target_file.exists():
            if hash_file.read_text() == current_hash:
                if build_data:
                    build_data["artifacts"].append(os.path.relpath(str(target_file), os.getcwd()))
                continue

        # レンダリングロジック
        config = yaml.safe_load(yaml_raw)
        dot_prefix = "." * (len(rel_path.parent.parts) + 1)
        classes_config = config.get("classes", {})
        current_mixins = set()

        for c_name, c in classes_config.items():
            current_mixins.update(c.get("mixins") or [])
            properties = c.get("properties") or {}
            for p_name, p_conf in properties.items():
                if p_conf is None: properties[p_name] = p_conf = {}
                p_conf["type"] = to_python_type(p_conf.get("type") or as2_registry.get(p_name, "Any"))
                
                field_args = ["kw_only=True"]
                if p_conf.get("alias"): field_args.append(f"alias='{p_conf['alias']}'")
                
                if "default" in p_conf: field_args.append(f"default={p_conf['default']}")
                elif "default_factory" in p_conf: field_args.append(f"default_factory={p_conf['default_factory']}")
                elif p_name == "type": field_args.append(f"default='{c_name}'")
                elif any(x in p_conf["type"] for x in ["None", "Optional", "|"]): field_args.append("default=None")
                elif "list[" in p_conf["type"].lower(): field_args.append("default_factory=list")
                elif "dict[" in p_conf["type"].lower(): field_args.append("default_factory=dict")
                else: field_args.append("default=None")

                p_conf["_rendered_field"] = f"Field({', '.join(field_args)})"

        rendered = template.render(
            classes=classes_config,
            dot_prefix=dot_prefix,
            mixins=sorted(list(current_mixins)),
            external_imports=config.get("imports", []),
        )

        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(rendered, encoding="utf-8")
        
        # ハッシュをキャッシュに保存
        hash_file.parent.mkdir(parents=True, exist_ok=True)
        hash_file.write_text(current_hash, encoding="utf-8")
        
        changed_files.append(str(target_file))
        print(f"--> Compiled: {target_file}")

        if build_data:
            build_data["artifacts"].append(os.path.relpath(str(target_file), os.getcwd()))

    if changed_files:
        print("--> Formatting with Ruff...")
        subprocess.run(["ruff", "check", "--select", "I,UP,B,F401", "--fix", output_root], capture_output=True)
        subprocess.run(["ruff", "format", output_root], capture_output=True)

class SchemaCompilerHook(BuildHookInterface):
    def initialize(self, version, build_data):
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