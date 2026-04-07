from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from apmodel.base import AS2Model

from apmodel._vendor.type_mapping import TYPE_MAPPING
from apmodel.inference import TypeInferencer

type_loader = TypeInferencer(TYPE_MAPPING)


def load(
    data: dict[str, Any], context: dict | None = None
) -> AS2Model | None:
    if context is None:
        context = data
        
    model_cls = type_loader.infer(data, parent_context=context)

    if model_cls is not None:
        return model_cls.model_validate(data, context=context)

    return None
