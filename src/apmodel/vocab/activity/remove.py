from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Remove(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Remove"
    type: Optional[str] = Field(default="Remove", kw_only=True, frozen=True)
