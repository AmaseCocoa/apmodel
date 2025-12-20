from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Reject(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Reject"
    type: Optional[str] = Field(default="Reject", kw_only=True, frozen=True)


class TentativeReject(Reject):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#TentativeReject"
    type: Optional[str] = Field(
        default="TentativeReject", kw_only=True, frozen=True
    )
