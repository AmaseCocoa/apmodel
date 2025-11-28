from pydantic import Field
from typing import Union

from ...types import Undefined
from ...core.activity import Activity


class Reject(Activity):
    type: Union[str, Undefined] = Field(default="Reject")


class TentativeReject(Reject):
    type: Union[str, Undefined] = Field(default="TentativeReject")
