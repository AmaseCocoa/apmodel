import datetime
from typing import Any, Optional, Union

from pydantic import Field, field_serializer

from ...core.activity import IntransitiveActivity
from ...core.link import Link
from ...core.object import Object


class Question(IntransitiveActivity):
    type: Optional[str] = Field(default="Question", kw_only=True, frozen=True)
    oneOf: Optional[Union[str, Object, Link]] = Field(default=None)
    anyOf: Optional[Union[str, Object, Link]] = Field(default=None)
    closed: Optional[Union[str, Object, Link, datetime.datetime, bool]] = Field(
        default=None
    )

    @field_serializer("closed", when_used="always")
    def serialize_closed(self, value: Any, _) -> Union[str, bool, Any]:
        if isinstance(value, datetime.datetime):
            return value.isoformat(timespec="seconds")

        return value
