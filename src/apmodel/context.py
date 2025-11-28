from __future__ import annotations

from typing import Any, Callable, Dict, List, TypeVar, Union, cast, overload

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

LDContextType = TypeVar("LDContextType", bound="LDContext")


class LDContext:
    """
    Parses and manages a JSON-LD @context, ensuring uniqueness.

    - String URLs are stored in a list, with duplicates ignored.
    - Dictionary definitions are merged, with later values overwriting earlier
      ones for the same key.
    This provides a list-like interface to the full context.
    """

    def __init__(self, context: Any = None):
        self.urls: List[str] = []
        self.definitions: Dict[str, Any] = {}
        if context:
            self.add(context)

    def _parse_and_add(self, context: Any):
        """Parses and adds a context item, handling deduplication."""
        if not isinstance(context, list):
            context = [context]

        for item in context:
            if isinstance(item, str):
                if item not in self.urls:
                    self.urls.append(item)
            elif isinstance(item, dict):
                self.definitions.update(item)

    def add(self, context: Any):
        """Adds a new item or list of items to the context."""
        self._parse_and_add(context)

    def remove(self, item: Union[str, dict]):
        """
        Removes an item from the context.
        - If item is a string, it's removed from the URL list.
        - If item is a dict, its keys are removed from the definitions.
        """
        if isinstance(item, str):
            if item in self.urls:
                self.urls.remove(item)
        elif isinstance(item, dict):
            for key in item:
                if key in self.definitions:
                    del self.definitions[key]

    @property
    def json(self) -> Dict[str, Any]:
        """
        Returns the merged dictionary of all JSON objects from the @context.
        """
        return self.definitions

    @property
    def full_context(self) -> List[Union[str, Dict[str, Any]]]:
        """
        Returns the full context as a list, with definitions merged into a single object.
        """
        result: List[Union[str, Dict[str, Any]]] = list(self.urls)
        if self.definitions:
            result.append(self.definitions)
        return result

    def __repr__(self) -> str:
        return f"LDContext({self.full_context})"

    def __len__(self) -> int:
        return len(self.full_context)

    def __iter__(self):
        return iter(self.full_context)

    @overload
    def __getitem__(self, key: int) -> Union[str, Dict[str, Any]]: ...

    @overload
    def __getitem__(self, key: slice) -> List[Union[str, Dict[str, Any]]]: ...

    def __getitem__(
        self, key: Union[int, slice]
    ) -> Union[Union[str, Dict[str, Any]], List[Union[str, Dict[str, Any]]]]:
        return self.full_context[key]

    def __add__(self: LDContextType, other: LDContext) -> LDContextType:
        """Merges two LDContext instances into a new one."""
        new_context = self.__class__(self.full_context)
        new_context.add(other.full_context)
        return new_context

    def __iadd__(self: LDContextType, other: LDContext) -> LDContextType:
        """Merges another LDContext instance into this one."""
        self.add(other.full_context)
        return self

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        validation_schema = core_schema.chain_schema(
            cast(
                List[CoreSchema],
                [
                    core_schema.any_schema(),
                    core_schema.no_info_plain_validator_function(cls._validate),
                ],
            )
        )

        serialization_schema = cast(Callable, core_schema.plain_serializer_function_ser)(
            cls._serialize,
            when_used="always",
            return_type=List[Union[str, Dict[str, Any]]],
        )

        return core_schema.json_or_python_schema(
            json_schema=validation_schema,
            python_schema=validation_schema,
            serialization=serialization_schema,
            metadata={"pydantic.internal.object_name": cls.__name__},
        )


    @classmethod
    def _validate(cls, value: Any) -> LDContext:
        if isinstance(value, cls):
            return value
        return cls(value)

    @staticmethod
    def _serialize(instance: LDContext) -> List[Union[str, Dict[str, Any]]]:
        return instance.full_context
