from typing import Union

from pydantic import Field

from ...core.activity import Activity
from ...types import Undefined


class Accept(Activity):
    type: Union[str, Undefined] = Field(default="Accept")


class TentativeAccept(Accept):
    type: Union[str, Undefined] = Field(default="TentativeAccept")
