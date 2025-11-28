from __future__ import annotations

from typing import TYPE_CHECKING, List, TypeVar, Union

from pydantic import Field

from ..context import LDContext
from ..dumper import _serialize_model_to_json
from ..types import ActivityPubModel, Undefined

if TYPE_CHECKING:
    from ..extra.emoji import Emoji
    from ..extra.hashtag import Hashtag
    from ..extra.schema import PropertyValue
    from ..vocab.actor import Actor
    from ..vocab.document import Image
    from .collection import Collection
    from .link import Link

T = TypeVar("T", bound="Object")


class Object(ActivityPubModel):
    _context: LDContext = Field(
        default_factory=lambda: LDContext(
            ["https://www.w3.org/ns/activitystreams"]
        ),
        kw_only=True,
    )
    id: Union[str, Undefined] = Field(default_factory=Undefined)
    type: Union[str, Undefined] = Field(default="Object", kw_only=True)
    name: Union[str, Undefined] = Field(default_factory=Undefined)
    content: Union[str, Undefined] = Field(default_factory=Undefined)
    summary: Union[str, Undefined] = Field(default_factory=Undefined)
    url: Union[str, "Link", Undefined] = Field(default_factory=Undefined)
    published: Union[str, Undefined] = Field(default_factory=Undefined)
    updated: Union[str, Undefined] = Field(default_factory=Undefined)
    attributedTo: Union[str, "Actor", List[Union[str, "Actor"]], Undefined] = (
        Field(default_factory=Undefined)
    )
    audience: Union[str, "Object", List[Union[str, "Object"]], Undefined] = (
        Field(default_factory=Undefined)
    )
    to: Union[str, "Object", List[Union[str, "Object"]], Undefined] = Field(
        default_factory=Undefined
    )
    bto: Union[str, "Object", List[Union[str, "Object"]], Undefined] = Field(
        default_factory=Undefined
    )
    cc: Union[str, "Object", List[Union[str, "Object"]], Undefined] = Field(
        default_factory=Undefined
    )
    bcc: Union[str, "Object", List[Union[str, "Object"]], Undefined] = Field(
        default_factory=Undefined
    )
    generator: Union["Object", Undefined] = Field(default_factory=Undefined)
    icon: Union["Image", Undefined] = Field(default_factory=Undefined)
    image: Union["Image", Undefined] = Field(default_factory=Undefined)
    inReplyTo: Union["Object", Undefined] = Field(default_factory=Undefined)
    location: Union["Object", Undefined] = Field(default_factory=Undefined)
    preview: Union["Object", Undefined] = Field(default_factory=Undefined)
    replies: Union["Collection", Undefined] = Field(default_factory=Undefined)
    scope: Union["Object", Undefined] = Field(default_factory=Undefined)
    tag: List[Union["Object", "Hashtag", "Emoji"]] = Field(default_factory=list)
    attachment: List[Union["Object", "PropertyValue"]] = Field(
        default_factory=list
    )
    _extra: dict = Field(default_factory=dict)

    def __post_init__(self):
        if self.type is Undefined:
            self.type = self.__class__.__name__

    def to_json(self):
        return _serialize_model_to_json(self)
