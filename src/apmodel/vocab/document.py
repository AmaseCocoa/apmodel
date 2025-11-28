from pydantic import Field
from typing import Union

from ..types import Undefined
from ..core.object import Object


class Document(Object):
    type: Union[str, Undefined] = Field(default="Document")


class Audio(Document):
    type: Union[str, Undefined] = Field(default="Audio")


class Image(Document):
    type: Union[str, Undefined] = Field(default="Image")


class Video(Document):
    type: Union[str, Undefined] = Field(default="Video")


class Page(Document):
    type: Union[str, Undefined] = Field(default="Page")