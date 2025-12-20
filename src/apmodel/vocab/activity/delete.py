from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Delete(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Delete"
    type: Optional[str] = Field(default="Delete", kw_only=True, frozen=True)
