from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypedDict, get_type_hints

from typing_extensions import Unpack

if TYPE_CHECKING:
    from apmodel.base import AS2Model


from apmodel._vendor.type_mapping import TYPE_MAPPING
from apmodel.inference import TypeInferencer

type_loader = TypeInferencer(TYPE_MAPPING)


class ExtraArgs(TypedDict, total=False):
    strict: bool | None
    extra: Literal["allow", "ignore", "forbid"] | None
    from_attributes: bool | None
    by_alias: bool | None
    by_name: bool | None


def load(data: dict, context: dict | None = None, **kwargs: Unpack[ExtraArgs]) -> AS2Model | None:
    if context is None:
        context = data

    model_cls: type[AS2Model] | None = type_loader.infer(data, parent_context=context)

    if model_cls is not None:
        allowed_keys = get_type_hints(ExtraArgs).keys()
        
        filtered = {
            k: v for k, v in kwargs.items() 
            if k in allowed_keys and v is not None
        }

        return model_cls.model_validate(data, context=context, **filtered)

    return None


load({})
