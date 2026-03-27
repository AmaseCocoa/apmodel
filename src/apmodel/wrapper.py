from pydantic_core import PydanticCustomError
from typing import TYPE_CHECKING, Annotated, TypeVar

from pydantic import BeforeValidator, ValidationInfo

from apmodel.loader import load

if TYPE_CHECKING:
    from apmodel.base import AS2Model

T = TypeVar("T", bound="AS2Model")


def parse_as2(model_cls: type[T], data: object, info: ValidationInfo) -> T | None:
    if isinstance(data, model_cls):
        return data

    if isinstance(data, dict):
        parent_context = None
        if info.data is not None and isinstance(info.data, dict):
            parent_context = info.data.get("@context")

        final_data = dict(data)
        if "@context" not in final_data and parent_context:
            final_data["@context"] = parent_context

        res = load(final_data, context=info.context)

        if isinstance(res, model_cls):
            return res
        return None

    return model_cls.model_validate(data)


if TYPE_CHECKING:
    WrapAS2 = Annotated[T, ...]
else:

    class WrapAS2:
        def __class_getitem__(cls, model_cls: type[T]) -> Annotated[T, ...]:
            def validator(v: object, i: ValidationInfo) -> T | None:
                result = parse_as2(model_cls, v, i)
                if not result:
                    raise PydanticCustomError("apmodel_parse_failed", "Failed to parse object")
                return parse_as2(model_cls, v, i)

            return Annotated[model_cls, BeforeValidator(validator)]
