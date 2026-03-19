from typing import TYPE_CHECKING, Any

from apmodel._vendor.tinyjld import TinyJLD, TinyJLDLoader

if TYPE_CHECKING:
    from apmodel.base import AS2Model


class TypeInferencer:
    def __init__(self, bootstrap: dict[str, str] | None = None) -> None:
        self.tjld = TinyJLD(loader=TinyJLDLoader())
        self.__cache: dict[str, type[AS2Model]] = {}
        self.__type_mapping: dict[str, str | type[AS2Model]] = dict(bootstrap or {})

    def set(self, key: str, cls: type["AS2Model"]) -> None:
        self.__type_mapping[key] = cls

    def _get(self, name: str) -> str | type["AS2Model"] | None:
        return self.__type_mapping.get(name)

    def infer(self, value: dict[str, Any]) -> type["AS2Model"] | None:
        if (val_type := self.tjld.resolve(value)) and (
            model_cls := self.__type_mapping.get(val_type)
        ):
            if isinstance(model_cls, str):
                if val_type not in self.__cache:
                    import importlib

                    mod_path, class_name = model_cls.rsplit(".", 1)
                    module = importlib.import_module(mod_path, "apmodel")
                    cls: type[AS2Model] = getattr(module, class_name)
                    cls.model_rebuild()
                    self.__cache[val_type] = cls
                else:
                    cls = self.__cache[val_type]
            else:
                cls = model_cls
            return cls
        return None
