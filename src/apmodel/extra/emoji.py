from typing import ClassVar, Optional

from pydantic import Field

from ..core.object import Object


class Emoji(Object):
    _model_type: ClassVar[str] = "http://joinmastodon.org/ns#Emoji"

    type: Optional[str] = Field(default="Emoji", kw_only=True, frozen=True)
