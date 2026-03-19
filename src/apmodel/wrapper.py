from typing import TYPE_CHECKING, Annotated, TypeVar, cast

from pydantic import BeforeValidator, ValidationInfo

from apmodel.loader import load

if TYPE_CHECKING:
    from apmodel.base import AS2Model

T = TypeVar("T", bound="AS2Model")


def parse_as2(model_cls: type[T], data: object, _: ValidationInfo) -> T | None:
    if isinstance(data, model_cls):
        return data

    if isinstance(data, dict):
        res = load(data)
        match res:
            case x if isinstance(x, model_cls):
                return cast("T", res)
            case _:
                return None

    return model_cls.model_validate(data)


if TYPE_CHECKING:
    WrapAS2 = Annotated[T, ...]
else:

    class WrapAS2:
        def __class_getitem__(cls, model_cls: type[T]) -> Annotated[T, ...]:
            def validator(v: object, i: ValidationInfo) -> T:
                return parse_as2(model_cls, v, i)

            return Annotated[model_cls, BeforeValidator(validator)]
