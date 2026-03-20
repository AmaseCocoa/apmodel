from typing import TypeVar

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PrivateAttr,
)

from apmodel.context import Context

T = TypeVar("T", bound="AS2Model")


def to_camel(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


class AS2Model(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, extra="allow", defer_build=True
    )
    _is_rebuilt: bool = PrivateAttr(default=False)

    ctx: Context = Field(alias="@context", kw_only=True)
