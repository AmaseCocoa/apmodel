from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Announce(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Announce"
    type: Optional[str] = Field(default="Announce", kw_only=True, frozen=True)
