from __future__ import annotations

from typing import Any, Dict, Iterable, List, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_serializer,
    model_validator,
)

ContextItem = Union[str, Dict[str, Any]]


class Context(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    urls: List[str] = Field(default_factory=list)
    definitions: Dict[str, Any] = Field(default_factory=dict)

    @staticmethod
    def _parse_input(data: Any) -> Dict[str, Any]:
        if isinstance(data, dict) and ("urls" in data or "definitions" in data):
            return data

        urls: List[str] = []
        definitions: Dict[str, Any] = {}

        def _recursive_parse(item: Any):
            if item is None:
                return
            if isinstance(item, Context):
                _recursive_parse(item.urls)
                _recursive_parse(item.definitions)
            elif isinstance(item, dict):
                definitions.update(item)
            elif isinstance(item, str):
                if item not in urls:
                    urls.append(item)
            elif isinstance(item, Iterable):
                for sub_item in item:
                    _recursive_parse(sub_item)

        _recursive_parse(data)
        return {"urls": urls, "definitions": definitions}

    @model_validator(mode="before")
    @classmethod
    def validate_to_internal_dict(cls, data: Any) -> Any:
        return cls._parse_input(data)

    def add(self, item: Any) -> None:
        updated = self._parse_input([self, item])
        self.urls = updated["urls"]
        self.definitions = updated["definitions"]

    def remove(self, item: Union[str, Dict[str, Any]]) -> None:
        if isinstance(item, str):
            if item in self.urls:
                self.urls.remove(item)
        elif isinstance(item, dict):
            for key in item:
                self.definitions.pop(key, None)

    @property
    def value(self) -> List[ContextItem]:
        result: List[ContextItem] = list(self.urls)
        if self.definitions:
            result.append(self.definitions)
        return result

    @model_serializer
    def serialize(self) -> Any:
        vals = self.value
        if not vals:
            return None
        return vals[0] if len(vals) == 1 else vals

    def __repr__(self) -> str:
        return f"Context({self.serialize()!r})"

    def __len__(self) -> int:
        return len(self.value)

    def __getitem__(self, index: int) -> ContextItem:
        return self.value[index]

    def __add__(self, other: Any) -> Context:
        return Context.model_validate([self, other])

    def __iadd__(self, other: Any) -> Context:
        self.add(other)
        return self
