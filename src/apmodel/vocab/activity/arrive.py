from pydantic import Field
from typing import Union

from ...types import Undefined
from ...core.activity import IntransitiveActivity


class Arrive(IntransitiveActivity):
    type: Union[str, Undefined] = Field(default="Arrive")
