from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Ignore(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Ignore"
    type: Optional[str] = Field(default="Ignore", kw_only=True, frozen=True)
