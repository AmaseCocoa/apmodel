from typing import TYPE_CHECKING, Any, Dict, Optional, Type

from ._vendor.tinyjld import TinyJLD, TinyJLDLoader

if TYPE_CHECKING:
    from .base import AS2Model


class TypeInferencer:
    def __init__(
        self, bootstrap: Optional[dict[str, type["AS2Model"]]] = None
    ) -> None:
        self.tjld = TinyJLD(loader=TinyJLDLoader())
        self.__type_mapping: Dict[str, type["AS2Model"]] = dict(bootstrap or {})

    def set(self, key, cls: Type["AS2Model"]) -> None:
        self.__type_mapping[key] = cls

    def _get(self, name: str) -> Type["AS2Model"] | None:
        return self.__type_mapping.get(name)

    def infer(self, value: dict[str, Any]) -> "AS2Model | None":
        if (val_type := self.tjld.resolve(value)) and (model_cls := self.__type_mapping.get(val_type)):
            return model_cls.model_validate(value)
        return None