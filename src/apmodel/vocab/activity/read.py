from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Read(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Read"
    type: Optional[str] = Field(default="Read", kw_only=True, frozen=True)
