from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Undo(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Undo"
    type: Optional[str] = Field(default="Undo", kw_only=True, frozen=True)
