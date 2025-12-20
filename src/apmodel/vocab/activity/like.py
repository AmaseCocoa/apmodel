from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Like(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Like"
    type: Optional[str] = Field(default="Like", kw_only=True, frozen=True)
