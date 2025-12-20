from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Follow(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Follow"
    type: Optional[str] = Field(default="Follow", kw_only=True, frozen=True)
