from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, TypeVar, Union

from pydantic import Field

from ..context import LDContext
from ..types import ActivityPubModel

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
        alias="@context"
    )
    id: str = Field()
    type: Optional[str] = Field(default="Object", kw_only=True, frozen=True)
    name: Optional[str] = Field(default=None)
    content: Optional[str] = Field(default=None)
    summary: Optional[str] = Field(default=None)
    url: Optional[Union[str, "Link"]] = Field(default=None)
    published: Optional[str] = Field(default=None)
    updated: Optional[str] = Field(default=None)
    attributedTo: Optional[Union[str, "Actor", List[Union[str, "Actor"]]]] = (
        Field(default=None)
    )
    audience: Optional[Union[str, "Object", List[Union[str, "Object"]]]] = (
        Field(default=None)
    )
    to: Optional[Union[str, "Object", List[Union[str, "Object"]]]] = Field(
        default=None
    )
    bto: Optional[Union[str, "Object", List[Union[str, "Object"]]]] = Field(
        default=None
    )
    cc: Optional[Union[str, "Object", List[Union[str, "Object"]]]] = Field(
        default=None
    )
    bcc: Optional[Union[str, "Object", List[Union[str, "Object"]]]] = Field(
        default=None
    )
    generator: Optional["Object"] = Field(default=None)
    icon: Optional["Image"] = Field(default=None)
    image: Optional["Image"] = Field(default=None)
    inReplyTo: Optional["Object"] = Field(default=None)
    location: Optional["Object"] = Field(default=None)
    preview: Optional["Object"] = Field(default=None)
    replies: Optional["Collection"] = Field(default=None)
    scope: Optional["Object"] = Field(default=None)
    tag: List[Union["Object", "Hashtag", "Emoji"]] = Field(default_factory=list)
    attachment: List[Union["Object", "PropertyValue"]] = Field(
        default_factory=list
    )
    _extra: dict = Field(default_factory=dict)