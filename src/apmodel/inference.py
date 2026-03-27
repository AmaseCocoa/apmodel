import importlib
import sys
import threading
import typing
from typing import Any

import pydantic

from apmodel._vendor.tinyjld import TinyJLD, TinyJLDLoader
from apmodel.base import AS2Model, ZDateTime


def generate_type_ns() -> dict:
    from apmodel import core
    from apmodel.wrapper import WrapAS2

    return {
        **vars(typing),
        **vars(pydantic),
        **vars(core),
        "WrapAS2": WrapAS2,
        "datetime": ZDateTime,
    }


class TypeInferencer:
    def __init__(self, bootstrap: dict[str, tuple[str, str]] | None = None) -> None:
        self.tjld = TinyJLD(loader=TinyJLDLoader())
        self.__cache: dict[str, type[AS2Model]] = {}
        self.__type_mapping: dict[str, tuple[str | type[AS2Model], str | None]] = dict(bootstrap or {})

        self.__lock = threading.Lock()

    def __rebuild_all(self, cls: type[AS2Model]) -> type[AS2Model]:
        for c in reversed(cls.__mro__):
            if isinstance(c, type) and issubclass(c, AS2Model) and c is not AS2Model:
                mod = sys.modules.get(c.__module__)
                if mod:
                    c.model_rebuild(_types_namespace={**generate_type_ns(), **vars(mod)})
        return cls

    def set(self, key: str, cls: type["AS2Model"]) -> None:
        with self.__lock:
            rebuilt_cls = self.__rebuild_all(cls)
            self.__type_mapping[key] = (rebuilt_cls, None)

    def _get(self, name: str) -> tuple[str | type[AS2Model] | None, str | None]:
        r = self.__type_mapping.get(name)
        if not r:
            return (None, None)
        return r

    def infer(
        self,
        value: dict[str, typing.Any],
        parent_context: dict[str, Any] | None = None,
    ) -> type["AS2Model"] | None:
        if val_type := self.tjld.resolve(value, parent_context=parent_context):
            if c := self.__cache.get(val_type):
                return c

            with self.__lock:
                if val_type in self.__cache:
                    return self.__cache[val_type]

                model_cls, parent = self._get(val_type)
                if not model_cls:
                    return None

                if isinstance(model_cls, str):
                    mod_path, class_name = model_cls.rsplit(".", 1)
                    module = importlib.import_module(mod_path, parent)
                    cls_obj = getattr(module, class_name)
                    if isinstance(cls_obj, type) and issubclass(cls_obj, AS2Model):
                        cls: type[AS2Model] = self.__rebuild_all(cls_obj)
                    else:
                        cls = cls_obj
                    self.__cache[val_type] = cls
                else:
                    cls = model_cls
                    self.__cache[val_type] = cls
            return cls
        return None
