from typing import Annotated, TypeAlias, TypeVar, Union

from pydantic import BaseModel, ConfigDict, Field, model_serializer

from .context import Context

T = TypeVar("T", bound="AS2Model")

AS2Value: TypeAlias = Annotated[Union[str, T], "as2_dispatch"]

def to_camel(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


class AS2Model(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, populate_by_name=True, extra="allow"
    )

    _context: Context = Field(alias="@context", kw_only=True)

    @model_serializer(mode="wrap")
    def _serialize_custom(self, handler, info):
        result = handler(self)

        if (
            info.exclude_defaults
            and "type" not in result
            and hasattr(self, "type")
        ):
            result["type"] = getattr(self, "type")

        if self.__pydantic_extra__:
            result.update(self.__pydantic_extra__)

        return result
