from typing import ClassVar, Optional

from pydantic import Field

from ..core.object import Object


class Document(Object):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Document"
    type: Optional[str] = Field(default="Document", kw_only=True, frozen=True)


class Audio(Document):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Audio"
    type: Optional[str] = Field(default="Audio", kw_only=True, frozen=True)


class Image(Document):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Image"
    type: Optional[str] = Field(default="Image", kw_only=True, frozen=True)


class Video(Document):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Video"
    type: Optional[str] = Field(default="Video", kw_only=True, frozen=True)


class Page(Document):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Page"
    type: Optional[str] = Field(default="Page", kw_only=True, frozen=True)
