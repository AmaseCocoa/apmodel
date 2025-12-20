from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class View(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#View"
    type: Optional[str] = Field(default="View", kw_only=True, frozen=True)
