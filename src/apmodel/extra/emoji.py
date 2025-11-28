from pydantic import Field
from typing import Union

from ..core import Object
from ..types import Undefined


class Emoji(Object):
    type: Union[str, Undefined] = Field(default="Emoji", kw_only=True)
    