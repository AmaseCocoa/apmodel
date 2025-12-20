from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Move(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Move"
    type: Optional[str] = Field(default="Move", kw_only=True, frozen=True)
