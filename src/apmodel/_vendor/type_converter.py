from typing import Any


def ensure_list(value: Any) -> Any: # noqa: ANN401
    if not isinstance(value, list):
        return [value]
    return value
