from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Accept(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Accept"
    type: Optional[str] = Field(default="Accept", kw_only=True, frozen=True)


class TentativeAccept(Accept):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#TentativeAccept"
    type: Optional[str] = Field(default="TentativeAccept", kw_only=True, frozen=True)
