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
        if info.context is not None and isinstance(info.context, dict):
            parent_context = info.context

        final_data = dict(data)
        if "@context" not in final_data and parent_context and "@context" in parent_context:
            final_data["@context"] = parent_context["@context"]

        res = load(final_data, context=parent_context)

        if isinstance(res, model_cls):
            return res

        if res is not None:
            return None

        if model_cls.__name__ == "Object":
            return data

        return None

    return model_cls.model_validate(data)


if TYPE_CHECKING:
    WrapAS2 = Annotated[T, ...]
else:

    class WrapAS2:
        def __class_getitem__(cls, model_cls: type[T]) -> Annotated[T, ...]:
            def validator(v: object, i: ValidationInfo) -> T | None:
                return parse_as2(model_cls, v, i)

            return Annotated[model_cls, BeforeValidator(validator)]
