from pydantic import Field
from typing import Union

from ...types import Undefined
from .offer import Offer


class Invite(Offer):
    type: Union[str, Undefined] = Field(default="Invite")
