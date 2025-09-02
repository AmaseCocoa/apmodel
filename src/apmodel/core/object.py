from __future__ import annotations

from dataclasses import dataclass, field, asdict, fields
from typing import List, Union, TypeVar, TYPE_CHECKING

from ..context import LDContext
from ..types import ActivityPubModel, Undefined

if TYPE_CHECKING:
    from .link import Link
    from .collection import Collection
    from ..vocab.actor import Actor
    from ..vocab.document import Image

T = TypeVar("T", bound="Object")

@dataclass
class Object(ActivityPubModel):
    _context: LDContext = field(default_factory=lambda: LDContext(["https://www.w3.org/ns/activitystreams"]), kw_only=True)
    id: Union[str, Undefined] = field(default_factory=Undefined)
    type: Union[str, Undefined] = field(default="Object", kw_only=True)
    name: Union[str, Undefined] = field(default_factory=Undefined)
    content: Union[str, Undefined] = field(default_factory=Undefined)
    summary: Union[str, Undefined] = field(default_factory=Undefined)
    url: Union[str, "Link", Undefined] = field(default_factory=Undefined)
    published: Union[str, Undefined] = field(default_factory=Undefined)
    updated: Union[str, Undefined] = field(default_factory=Undefined)
    attributedTo: Union[str, "Actor", List[Union[str, "Actor"]], Undefined] = field(default_factory=Undefined)
    audience: Union[str, "Object", List[Union[str, "Object"]], Undefined] = field(default_factory=Undefined)
    to: Union[str, "Object", List[Union[str, "Object"]], Undefined] = field(default_factory=Undefined)
    bto: Union[str, "Object", List[Union[str, "Object"]], Undefined] = field(default_factory=Undefined)
    cc: Union[str, "Object", List[Union[str, "Object"]], Undefined] = field(default_factory=Undefined)
    bcc: Union[str, "Object", List[Union[str, "Object"]], Undefined] = field(default_factory=Undefined)
    generator: Union["Object", Undefined] = field(default_factory=Undefined)
    icon: Union["Image", Undefined] = field(default_factory=Undefined)
    image: Union["Image", Undefined] = field(default_factory=Undefined)
    inReplyTo: Union["Object", Undefined] = field(default_factory=Undefined)
    location: Union["Object", Undefined] = field(default_factory=Undefined)
    preview: Union["Object", Undefined] = field(default_factory=Undefined)
    replies: Union["Collection", Undefined] = field(default_factory=Undefined)
    scope: Union["Object", Undefined] = field(default_factory=Undefined)
    tag: List["Object"] = field(default_factory=list)
    attachment: List["Object"] = field(default_factory=list)
    _extra: dict = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.type, Undefined):
            self.type = self.__class__.__name__

    

    def to_json(self):
        # This method manually serializes the dataclass to correctly handle
        # recursive context aggregation without using asdict.
        
        # Start with this object's context.
        aggregated_context = self._context

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
                    aggregated_context += value._context
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
                            aggregated_context += item._context
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