from typing import ClassVar, Optional

from pydantic import Field

from ..core.object import Object


class Note(Object):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Note"
    type: Optional[str] = Field(default="Note", kw_only=True, frozen=True)
