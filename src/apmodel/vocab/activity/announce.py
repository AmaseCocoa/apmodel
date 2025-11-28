from pydantic import Field
from typing import Union

from ...types import Undefined
from ...core.activity import Activity


class Announce(Activity):
    type: Union[str, Undefined] = Field(default="Announce")
