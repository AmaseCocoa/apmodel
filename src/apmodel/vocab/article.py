from pydantic import Field
from typing import Union
from ..types import Undefined
from ..core.object import Object


class Article(Object):
    type: Union[str, Undefined] = Field(default="Article")
