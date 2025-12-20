from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import IntransitiveActivity


class Arrive(IntransitiveActivity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#"
    type: Optional[str] = Field(default="Arrive", kw_only=True, frozen=True)
