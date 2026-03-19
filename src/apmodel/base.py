from typing import Annotated, Any, TypeVar

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PrivateAttr,
    TypeAdapter,
)

from apmodel.context import Context

T = TypeVar("T", bound="AS2Model")


def load_as2model(v: Any) -> "AS2Model":
    processed = v
    if isinstance(v, dict):
        processed = {k.lower(): val for k, val in v.items()}

    return TypeAdapter(model_cls).validate_python(processed)


WrapAS2 = Annotated[T, BeforeValidator(load_as2model)]


def to_camel(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


class AS2Model(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, extra="allow", defer_build=True
    )
    _is_rebuilt: bool = PrivateAttr(False)

    ctx: Context = Field(alias="@context", kw_only=True)
