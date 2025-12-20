from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Leave(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Leave"
    type: Optional[str] = Field(default="Leave", kw_only=True, frozen=True)
