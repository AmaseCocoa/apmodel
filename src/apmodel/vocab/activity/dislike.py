from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Dislike(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Dislike"
    type: Optional[str] = Field(default="Dislike", kw_only=True, frozen=True)
