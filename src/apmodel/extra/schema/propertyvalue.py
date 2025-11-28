from pydantic import Field
from typing import Union

from ...types import Undefined, ActivityPubModel


class PropertyValue(ActivityPubModel):
    type: Union[str, Undefined] = Field(default="PropertyValue", kw_only=True)

    name: Union[str, Undefined] = Field(default_factory=Undefined)
    value: Union[str, Undefined] = Field(default_factory=Undefined)

    _extra: dict = Field(default_factory=dict)