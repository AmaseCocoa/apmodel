import os
import subprocess
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader


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
        "datetime",
    }
    if "|" in type_str or "[" in type_str:
        return f"'{type_str}'"
    if type_str in well_known:
        return type_str
    return f"'{type_str}'"


def generate_all(schema_root: str, output_root: str, template_dir: str):
    env = Environment(loader=FileSystemLoader(template_dir))
    env.filters["to_snake"] = to_snake
    env.filters["mixin_to_file"] = mixin_to_file
    env.filters["to_python_type"] = to_python_type

    template = env.get_template("model.py.j2")

    schema_path = Path(schema_root)
    output_path = Path(output_root)

    for yaml_file in schema_path.rglob("*.yaml"):
        with open(yaml_file, "r") as f:
            config = yaml.safe_load(f)

        rel_to_root = yaml_file.relative_to(schema_path).parent
        depth = len(rel_to_root.parts)
        dot_prefix = "." * (depth + 1)

        current_mixins = set()
        for c in config.get("classes", {}).values():
            mixins = c.get("mixins") or []
            current_mixins.update(mixins)

        target_file = output_path / rel_to_root / f"{yaml_file.stem}.py"
        target_file.parent.mkdir(parents=True, exist_ok=True)

        rendered = template.render(
            classes=config.get("classes", {}),
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


if __name__ == "__main__":
    generate_all("schemas", "src/apmodel", "templates")
