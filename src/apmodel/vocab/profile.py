from pydantic import Field
from typing import Union
from ..types import Undefined
from ..core.object import Object


class Profile(Object):
    type: Union[str, Undefined] = Field(default="Profile")
    describes: Object | Undefined = Field(default_factory=Undefined)