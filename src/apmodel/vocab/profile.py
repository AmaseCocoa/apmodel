from typing import ClassVar, Optional

from pydantic import Field

from ..core.object import Object


class Profile(Object):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Profile"
    type: Optional[str] = Field(default="Profile", kw_only=True, frozen=True)
    describes: Optional[Object] = Field(default=None)
