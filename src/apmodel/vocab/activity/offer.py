from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Offer(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Offer"
    type: Optional[str] = Field(default="Offer", kw_only=True, frozen=True)
