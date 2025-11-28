from pydantic import Field
from typing import Union

from ...types import Undefined
from ...core.activity import Activity


class Like(Activity):
    type: Union[str, Undefined] = Field(default="Like")
