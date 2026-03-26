import datetime
from typing import Annotated, TypeAlias, TypeVar

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PlainSerializer,
    PrivateAttr,
)

from apmodel.context import Context

T = TypeVar("T", bound="AS2Model")
ZDateTime: TypeAlias = Annotated[
    datetime.datetime,
    PlainSerializer(
        lambda v: (
            (v if v.tzinfo else v.replace(tzinfo=datetime.timezone.utc))
            .astimezone(datetime.timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )
    ),
]


def to_camel(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


class AS2Model(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="allow",
        defer_build=True,
    )
    _is_rebuilt: bool = PrivateAttr(default=False)

    ctx: Context | None = Field(
        alias="@context", kw_only=True, default=None
    )
