from __future__ import annotations

from typing import Any, Dict, Iterable, List, Union

from pydantic import (
    BaseModel,
    Field,
    model_serializer,
    model_validator,
)

ContextItem = Union[str, Dict[str, Any]]


class Context(BaseModel):

    urls: List[str] = Field(default_factory=list)
    definitions: Dict[str, Any] = Field(default_factory=dict)

    def __init__(self, context: Any = None, **data: Any):
        super().__init__(**data)
        if context is not None:
            self.add(context)

    def add(self, context: Any) -> None:
        if context is None:
            return

        if isinstance(context, Context):
            self.add(context.urls)
            self.add(context.definitions)
            return

        if isinstance(context, dict):
            self.definitions.update(context)
            return

        if isinstance(context, str):
            if context not in self.urls:
                self.urls.append(context)
            return

        if isinstance(context, Iterable):
            for item in context:
                self.add(item)

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

    @model_validator(mode="before")
    @classmethod
    def validate_input(cls, value: Any) -> Dict[str, Any]:
        if isinstance(value, dict) and (
            "urls" in value or "definitions" in value
        ):
            return value

        instance = cls()
        instance.add(value)
        return {"urls": instance.urls, "definitions": instance.definitions}

    @model_serializer
    def serialize(self) -> Any:
        vals = self.value
        if not vals:
            return None
        if len(vals) == 1:
            return vals[0]
        return vals

    def __repr__(self) -> str:
        return f"Context({self.serialize()})"

    def __len__(self) -> int:
        return len(self.value)

    def __getitem__(self, index: int) -> ContextItem:
        return self.value[index]

    def __add__(self, other: Any) -> Context:
        new_instance = Context(self.value)
        new_instance.add(other)
        return new_instance

    def __iadd__(self, other: Any) -> Context:
        self.add(other)
        return self
