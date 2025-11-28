from pydantic import Field
from typing import Union

from ...types import Undefined
from .ignore import Ignore


class Block(Ignore):
    type: Union[str, Undefined] = Field(default="Block")
