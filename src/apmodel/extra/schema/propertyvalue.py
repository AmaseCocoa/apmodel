from pydantic import Field
from typing import Union

from ...dumper import _serialize_model_to_json
from ...types import ActivityPubModel, Undefined



class PropertyValue(ActivityPubModel):
    type: Union[str, Undefined] = Field(default="PropertyValue", kw_only=True)

    name: Union[str, Undefined] = Field(default_factory=Undefined)
    value: Union[str, Undefined] = Field(default_factory=Undefined)

    _extra: dict = Field(default_factory=dict)

    def to_json(self) -> dict:
        return _serialize_model_to_json(self)
