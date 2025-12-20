from typing import ClassVar, Optional

from pydantic import Field

from ...core.activity import Activity


class Update(Activity):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Update"
    type: Optional[str] = Field(default="Update", kw_only=True, frozen=True)
