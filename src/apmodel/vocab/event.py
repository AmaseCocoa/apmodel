from typing import Literal, Union
from dataclasses import field, dataclass

from ..types import Undefined
from ..core.object import Object


class Event(Object):
    type: Union[str, Undefined] = Field(default="Event")


class Place(Object):
    type: Union[str, Undefined] = Field(default="Place")
    accuracy: float | Undefined = Field(default_factory=Undefined)
    altitude: float | Undefined = Field(default_factory=Undefined)
    latitude: float | Undefined = Field(default_factory=Undefined)
    longitude: float | Undefined = Field(default_factory=Undefined)
    radius: float | Undefined = Field(default_factory=Undefined)
    units: str | Literal["cm", "feet", "inches", "km", "m", "miles"] | Undefined = Field(default_factory=Undefined)