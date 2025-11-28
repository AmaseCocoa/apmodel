from dataclasses import dataclass, field
from typing import Union

from ...dumper import _serialize_model_to_json
from ...types import ActivityPubModel, Undefined


@dataclass
class PropertyValue(ActivityPubModel):
    type: Union[str, Undefined] = field(default="PropertyValue", kw_only=True)

    name: Union[str, Undefined] = field(default_factory=Undefined)
    value: Union[str, Undefined] = field(default_factory=Undefined)

    _extra: dict = field(default_factory=dict)

    def to_json(self) -> dict:
        return _serialize_model_to_json(self)
