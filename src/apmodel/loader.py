from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Mapping,
    Optional,
    Type,
)

if TYPE_CHECKING:
    from apmodel.base import AS2Model


from apmodel.inference import TypeInferencer

type_loader = TypeInferencer(
    {
        "https://www.w3.org/ns/activitystreams#Create": "apmodel.activities.create.Create"
    }
)


def load(
    data: dict, 
    *args: object, 
    **kwargs: object
) -> Optional["AS2Model"]:
    model_cls: Optional[Type["AS2Model"]] = type_loader.infer(data)
    
    if model_cls is not None:
        return model_cls.model_validate(data, *args, **kwargs)
    
    return None
