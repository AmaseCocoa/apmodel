from pydantic import Field
from typing import Union

from ...types import Undefined
from ...core.activity import Activity


class Delete(Activity):
    type: Union[str, Undefined] = Field(default="Delete")
