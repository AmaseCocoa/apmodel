from typing import ClassVar, Optional

from pydantic import Field

from .offer import Offer


class Invite(Offer):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Invite"
    type: Optional[str] = Field(default="Invite", kw_only=True, frozen=True)
