from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, TypeVar

from pydantic import Field, ValidationInfo, field_validator
from typing_extensions import Dict

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
        alias="@context",
    )
    id: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default="Object", kw_only=True, frozen=True)
    name: Optional[str] = Field(default=None)
    content: Optional[str] = Field(default=None)
    summary: Optional[str] = Field(default=None)
    url: Optional["str | Link"] = Field(default=None)
    published: Optional[str] = Field(default=None)
    updated: Optional[str] = Field(default=None)
    attributed_to: Optional["str | Actor | List[str | Actor]"] = Field(
        default=None
    )
    audience: Optional["str | Object | Dict[str, Any] | List[str | Object]"] = (
        Field(default=None)
    )
    to: Optional[
        "str | Object | Dict[str, Any] | List[str | Object | Dict[str, Any]]"
    ] = Field(default=None)
    bto: Optional[
        "str | Object | Dict[str, Any] | List[str | Object | Dict[str, Any]]"
    ] = Field(default=None)
    cc: Optional[
        "str | Object | Dict[str, Any] | List[str | Object | Dict[str, Any]]"
    ] = Field(default=None)
    bcc: Optional[
        "str | Object | Dict[str, Any] | List[str | Object | Dict[str, Any]]"
    ] = Field(default=None)
    generator: "Optional[Object | Dict[str, Any]]" = Field(default=None)
    icon: Optional["Image"] = Field(default=None)
    image: Optional["Image"] = Field(default=None)
    in_reply_to: "Optional[Object | Dict[str, Any]]" = Field(default=None)
    location: "Optional[Object | Dict[str, Any]]" = Field(default=None)
    preview: "Optional[Object | Dict[str, Any]]" = Field(default=None)
    replies: Optional["Collection"] = Field(default=None)
    scope: "Optional[Object | Dict[str, Any]]" = Field(default=None)
    tag: "List[Object | Hashtag | Emoji | Dict[str, Any]]" = Field(
        default_factory=list
    )
    attachment: "List[PropertyValue | Dict[str, Any] | Object | Link]" = Field(
        default_factory=list
    )

    @classmethod
    def _convert_field_to_model(cls, v: Any, info: ValidationInfo) -> Any:
        from ..loader import load

        if v is None:
            return None
        parent_context = (
            info.context.get("ld_context") if info.context else None
        )
        return load(v, "raw", parent_context=parent_context)

    @field_validator("url", mode="before")
    @classmethod
    def validate_url(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

    @field_validator("attributed_to", mode="before")
    @classmethod
    def validate_attributed_to(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

    @field_validator("audience", mode="before")
    @classmethod
    def def_validate_audience(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

    @field_validator("to", mode="before")
    @classmethod
    def validate_to(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

    @field_validator("bto", mode="before")
    @classmethod
    def validate_bto(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

    @field_validator("cc", mode="before")
    @classmethod
    def validate_cc(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

    @field_validator("bcc", mode="before")
    @classmethod
    def validate_bcc(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

    @field_validator("generator", mode="before")
    @classmethod
    def validate_generator(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

    @field_validator("icon", mode="before")
    @classmethod
    def validate_icon(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

    @field_validator("image", mode="before")
    @classmethod
    def validate_image(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

    @field_validator("in_reply_to", mode="before")
    @classmethod
    def validate_in_reply_to(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

    @field_validator("location", mode="before")
    @classmethod
    def validate_location(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

    @field_validator("preview", mode="before")
    @classmethod
    def validate_preview(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

    @field_validator("replies", mode="before")
    @classmethod
    def validate_replies(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

    @field_validator("scope", mode="before")
    @classmethod
    def validate_scope(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

    @field_validator("tag", mode="before")
    @classmethod
    def validate_tag(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)

    @field_validator("attachment", mode="before")
    @classmethod
    def validate_attachment(cls, v: Any, info: ValidationInfo) -> Any:
        return cls._convert_field_to_model(v, info)
