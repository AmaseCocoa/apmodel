from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apmodel.base import AS2Model


from apmodel.inference import TypeInferencer

type_loader = TypeInferencer(
    {
        "https://www.w3.org/ns/activitystreams#Create": "apmodel.activities.create.Create"
    }
)


def load(data: dict, *args: object, **kwargs: object) -> AS2Model | None:
    model_cls: type[AS2Model] | None = type_loader.infer(data)

    if model_cls is not None:
        return model_cls.model_validate(data, *args, **kwargs)

    return None
