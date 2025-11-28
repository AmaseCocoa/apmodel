import datetime
from typing import Any, Optional, Union

from pydantic import Field, field_serializer, field_validator

from ..core.object import Object

DeletedTypes = Optional[Union[datetime.datetime, str]]


class Tombstone(Object):
    type: Optional[str] = Field(default="Tombstone", kw_only=True, frozen=True)
    formerType: Optional[Union[str, Object]] = Field(default=None)
    deleted: Optional[Union[datetime.datetime, str]] = Field(default=None)

    @field_validator("deleted", mode="before")
    @classmethod
    def parse_deleted_datetime(cls, v: Any) -> DeletedTypes:
        if v is None or not isinstance(v, str):
            return v

        try:
            iso_string = v.replace("Z", "+00:00")
            return datetime.datetime.fromisoformat(iso_string)
        except ValueError as e:
            raise ValueError(
                f"Invalid ISO 8601 format for 'deleted' field: {v}. Error: {e}"
            )

    @field_serializer("deleted", when_used="always")
    def serialize_deleted_datetime(
        self, value: DeletedTypes, _
    ) -> Union[str, Any]:
        if isinstance(value, datetime.datetime):
            iso_string = value.isoformat(timespec="seconds")
            return iso_string.replace("+00:00", "Z")

        return value
