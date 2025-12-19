from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Create(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Create"
    type: Optional[str] = Field(default="Create", kw_only=True, frozen=True)
