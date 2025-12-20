from typing import ClassVar, Optional

from pydantic import Field

from .ignore import Ignore


class Block(Ignore):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Block"
    type: Optional[str] = Field(default="Block", kw_only=True, frozen=True)
