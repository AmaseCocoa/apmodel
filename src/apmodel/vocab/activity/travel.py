from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import IntransitiveActivity


class Travel(IntransitiveActivity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Travel"
    type: Optional[str] = Field(default="Travel", kw_only=True, frozen=True)
