from typing import ClassVar, Optional

from pydantic import Field

from ..core.link import Link


class Mention(Link):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Mention"
    type: Optional[str] = Field(default="Mention", kw_only=True, frozen=True)
