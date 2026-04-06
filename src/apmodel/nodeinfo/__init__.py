# compile: skip
from apmodel.nodeinfo.nodeinfo import Nodeinfo


def from_dict(obj: dict) -> Nodeinfo:
    return Nodeinfo.model_validate(obj)