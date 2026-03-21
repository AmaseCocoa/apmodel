import importlib
import sys
import threading
import typing

import pydantic

from apmodel._vendor.tinyjld import TinyJLD, TinyJLDLoader
from apmodel.base import AS2Model, ZDateTime

TYPE_NS = {**vars(typing), **vars(pydantic), "datetime": ZDateTime}


class TypeInferencer:
    def __init__(self, bootstrap: dict[str, str] | None = None) -> None:
        self.tjld = TinyJLD(loader=TinyJLDLoader())
        self.__cache: dict[str, type[AS2Model]] = {}
        self.__type_mapping: dict[str, str | type[AS2Model]] = dict(
            bootstrap or {}
        )

        self.__lock = threading.Lock()

    def __rebuild_all(self, cls: type[AS2Model]) -> type[AS2Model]:
        for c in reversed(cls.__mro__):
            if (
                isinstance(c, type)
                and issubclass(c, AS2Model)
                and c is not AS2Model
            ):
                mod = sys.modules.get(c.__module__)
                if mod:
                    c.model_rebuild(_types_namespace={**TYPE_NS, **vars(mod)})
        return cls

    def set(self, key: str, cls: type["AS2Model"]) -> None:
        with self.__lock:
            rebuilt_cls = self.__rebuild_all(cls)
            self.__type_mapping[key] = rebuilt_cls

    def _get(self, name: str) -> str | type["AS2Model"] | None:
        return self.__type_mapping.get(name)

    def infer(self, value: dict[str, typing.Any]) -> type["AS2Model"] | None:
        if val_type := self.tjld.resolve(value):
            if c := self.__cache.get(val_type):
                return c

            with self.__lock:
                if val_type in self.__cache:
                    return self.__cache[val_type]

                if not (model_cls := self.__type_mapping.get(val_type)):
                    return None

                if isinstance(model_cls, str):
                    mod_path, class_name = model_cls.rsplit(".", 1)
                    module = importlib.import_module(mod_path, "apmodel")
                    cls: type[AS2Model] = self.__rebuild_all(
                        getattr(module, class_name)
                    )
                    self.__cache[val_type] = cls
                else:
                    cls = model_cls
            return cls
        return None
