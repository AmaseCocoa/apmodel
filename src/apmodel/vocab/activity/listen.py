from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Listen(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Listen"
    type: Optional[str] = Field(default="Listen", kw_only=True, frozen=True)
