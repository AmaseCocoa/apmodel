from typing import ClassVar, Optional

from pydantic import Field

from ..core.link import Link


class Hashtag(Link):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Hashtag"
    type: Optional[str] = Field(default="Hashtag", kw_only=True, frozen=True)
