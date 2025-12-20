from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Add(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Add"
    type: Optional[str] = Field(default="Add", kw_only=True, frozen=True)
