from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union, List

from .object import Object
from ..types import Undefined

@dataclass
class Activity(Object):
    type: Union[str, Undefined] = field(default="Activity", kw_only=True)

    actor: Union[str, "Actor", List[Union[str, "Actor"]], Undefined] = field(default_factory=Undefined)
    object: Union[Object, Undefined] = field(default_factory=Undefined)
    target: Union[str, "Actor", List[Union[str, "Actor"]], Undefined] = field(default_factory=Undefined)
    result: Union[dict, Undefined] = field(default_factory=Undefined)
    origin: Union[dict, Undefined] = field(default_factory=Undefined)
    instrument: Union[dict, Undefined] = field(default_factory=Undefined)

@dataclass
class IntransitiveActivity(Object):
    type: Union[str, Undefined] = field(default="Activity", kw_only=True)

    actor: Union[str, "Actor", List[Union[str, "Actor"]], Undefined] = field(default_factory=Undefined)
    object: Union[Object, Undefined] = field(default_factory=Undefined)
    target: Union[str, "Actor", List[Union[str, "Actor"]], Undefined] = field(default_factory=Undefined)
    result: Union[dict, Undefined] = field(default_factory=Undefined)
    instrument: Union[dict, Undefined] = field(default_factory=Undefined)