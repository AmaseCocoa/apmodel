from pydantic import Field
from typing import Union

from ..core.link import Link
from ..types import Undefined


class Hashtag(Link):
    type: Union[str, Undefined] = Field(default="Hashtag", kw_only=True)
