import json
from .core import Object

def dump(model: Object, **kwargs) -> str:
    return json.dumps(model.to_json(), **kwargs)
