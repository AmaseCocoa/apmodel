import datetime
from typing import Any, Optional

from pydantic import Field, field_serializer

from ...core.activity import IntransitiveActivity
from ...core.link import Link
from ...core.object import Object


class Question(IntransitiveActivity):
    type: Optional[str] = Field(default="Question", kw_only=True, frozen=True)
    one_of: Optional[str | Object | Link] = Field(default=None)
    any_of: Optional[str | Object | Link] = Field(default=None)
    closed: Optional[str | Object | Link | datetime.datetime | bool] = Field(
        default=None
    )

    @field_serializer("closed", when_used="always")
    def serialize_closed(self, value: Any, _) -> str | bool | Any:
        if isinstance(value, datetime.datetime):
            return value.isoformat(timespec="seconds")

        return value
