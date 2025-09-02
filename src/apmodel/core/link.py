from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Union, TYPE_CHECKING, TypeVar

from ..context import LDContext
from ..types import Undefined, ActivityPubModel

if TYPE_CHECKING:
    from .object import Object

T = TypeVar("T", bound="Link")

@dataclass
class Link(ActivityPubModel):
    _context: LDContext = field(default=LDContext(["https://www.w3.org/ns/activitystreams"]), kw_only=True)

    type: Union[str, Undefined] = field(default="Link", kw_only=True)
    id: Union[str, "Object", Link, Undefined] = field(default="Link", kw_only=True)
    name: Union[str, Undefined] = field(default="Link", kw_only=True)
    href: Union[str, Undefined] = field(default_factory=Undefined)
    hreflang: Union[str, Undefined] = field(default_factory=Undefined)
    mediaType: Union[str, Undefined] = field(default_factory=Undefined)
    
    _extra: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.type is Undefined:
            self.type = self.__class__.__name__

    

    def to_json(self):
        data = asdict(self)
        extra = data.pop("_extra", {})
        ctx = data.pop("_context")
        if isinstance(ctx, LDContext):
            data["@context"] = ctx.full_context
        else:
            data["@context"] = ctx
        for key, value in list(data.items()):
            if isinstance(value, Undefined):
                del data[key]
            elif isinstance(value, ActivityPubModel) or isinstance(value, Link):
                data[key] = value.to_json()
            elif isinstance(value, list):
                data[key] = [v.to_json() if isinstance(v, ActivityPubModel) else v for v in value]
        data.update(extra)
        return data