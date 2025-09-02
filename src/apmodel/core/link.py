from __future__ import annotations

from dataclasses import dataclass, field, fields
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
    id: Union[str, "Object", Link, Undefined] = field(default_factory=Undefined, kw_only=True)
    name: Union[str, Undefined] = field(default_factory=Undefined, kw_only=True)
    href: Union[str, Undefined] = field(default_factory=Undefined)
    hreflang: Union[str, Undefined] = field(default_factory=Undefined)
    mediaType: Union[str, Undefined] = field(default_factory=Undefined)
    
    _extra: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.type is Undefined:
            self.type = self.__class__.__name__

    

    def to_json(self):
        # Start with this object's context. Create a new instance to avoid modifying self._context.
        aggregated_context = self._context + LDContext()

        data = {}
        # Manually iterate over the fields of this dataclass instance.
        # fields() correctly includes fields from parent and child classes.
        for f in fields(self):
            value = getattr(self, f.name)

            # Skip private fields and undefined values.
            if f.name.startswith('_') or isinstance(value, Undefined):
                continue

            # Recursively serialize nested ActivityPubModels.
            if isinstance(value, ActivityPubModel):
                # Aggregate context from the child model.
                if hasattr(value, '_context') and value._context:
                    aggregated_context = aggregated_context + value._context
                # Serialize the child, which will produce a dict.
                child_json = value.to_json()
                # The child's context is not needed since we aggregated it.
                child_json.pop("@context", None)
                data[f.name] = child_json
            elif isinstance(value, list):
                processed_list = []
                for item in value:
                    if isinstance(item, ActivityPubModel):
                        if hasattr(item, '_context') and item._context:
                            aggregated_context = aggregated_context + item._context
                        child_json = item.to_json()
                        child_json.pop("@context", None)
                        processed_list.append(child_json)
                    else:
                        processed_list.append(item)
                data[f.name] = processed_list
            else:
                data[f.name] = value

        # Add the final, fully merged context and any extra properties.
        data["@context"] = aggregated_context.full_context
        if self._extra:
            data.update(self._extra)
            
        return data