from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypeVar, Union

from pydantic import Field

from ..context import LDContext
from ..types import ActivityPubModel

if TYPE_CHECKING:
    from .object import Object

T = TypeVar("T", bound="Link")


class Link(ActivityPubModel):
    _context: LDContext = Field(
        default_factory=lambda: LDContext(
            ["https://www.w3.org/ns/activitystreams"]
        ),
        kw_only=True,
        alias="@context"
    )

    type: Optional[str] = Field(default="Link", kw_only=True, frozen=True)
    id: Optional[Union[str, "Object", Link]] = Field(default=None, kw_only=True)
    name: Optional[str] = Field(default=None, kw_only=True)
    href: Optional[str] = Field(default=None)
    hreflang: Optional[str] = Field(default=None)
    mediaType: Optional[str] = Field(default=None)

    _extra: dict = Field(default_factory=dict)