import sys
from typing import TYPE_CHECKING, Any, Dict, Type

from ._vendor.tinyjld import TinyJLD, TinyJLDLoader

if TYPE_CHECKING:
    from .base import AS2Model


class TypeInferencer:
    def __init__(self) -> None:
        loader = TinyJLDLoader()
        self.tjld = TinyJLD(loader=loader)
        self.__type_mapping: Dict[str, type["AS2Model"]] = {}

    def _set(self, key, cls: Type["AS2Model"]) -> None:
        self.__type_mapping[sys.intern(key)] = cls

    def _get(self, name: str) -> Type["AS2Model"] | None:
        return self.__type_mapping.get(sys.intern(name))

    def infer(self, value: dict[str, Any]) -> "AS2Model | None":
        val_type = self.tjld.resolve(value)
        if not val_type:
            return None
        res = self._get(val_type)
        if not res:
            return None
        return res.model_validate(value)
