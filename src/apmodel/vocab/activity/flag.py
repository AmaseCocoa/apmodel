from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Flag(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Flag"
    type: Optional[str] = Field(default="Flag", kw_only=True, frozen=True)
