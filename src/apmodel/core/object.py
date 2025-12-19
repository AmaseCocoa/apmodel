from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, TypeVar

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
    context: LDContext = Field(
        default_factory=lambda: LDContext(
            ["https://www.w3.org/ns/activitystreams"]
        ),
        kw_only=True,
        alias="@context"
    )
    id: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default="Object", kw_only=True, frozen=True)
    name: Optional[str] = Field(default=None)
    content: Optional[str] = Field(default=None)
    summary: Optional[str] = Field(default=None)
    url: Optional["str | Link"] = Field(default=None)
    published: Optional[str] = Field(default=None)
    updated: Optional[str] = Field(default=None)
    attributed_to: Optional["str | Actor | List[str | Actor]"] = (
        Field(default=None)
    )
    audience: Optional["str | Object | List[str | Object]"] = (
        Field(default=None)
    )
    to: Optional["str | Object | List[str | Object]"] = Field(
        default=None
    )
    bto: Optional["str | Object | List[str | Object]"] = Field(
        default=None
    )
    cc: Optional["str | Object | List[str | Object]"] = Field(
        default=None
    )
    bcc: Optional["str | Object | List[str | Object]"] = Field(
        default=None
    )
    generator: Optional["Object"] = Field(default=None)
    icon: Optional["Image"] = Field(default=None)
    image: Optional["Image"] = Field(default=None)
    in_reply_to: Optional["Object"] = Field(default=None)
    location: Optional["Object"] = Field(default=None)
    preview: Optional["Object"] = Field(default=None)
    replies: Optional["Collection"] = Field(default=None)
    scope: Optional["Object"] = Field(default=None)
    tag: List["Object | Hashtag | Emoji"] = Field(default_factory=list)
    attachment: List["Object | PropertyValue"] = Field(
        default_factory=list
    )