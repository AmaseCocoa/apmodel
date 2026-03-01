from __future__ import annotations

from typing import Any, Dict, Type, TypeVar, Union

from snaplet import SnapletBase

T = TypeVar("T", bound="AS2Model")


class AS2Model(SnapletBase):
    """
    Base class for all ActivityPub models.
    """

    def __init__(self, data: Dict[str, Any] | None = None):
        super().__init__(data if data is not None else {})

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        return cls(data)

    def _wrap_value(self, value: Any) -> Any:
        """
        Wrap a dict value into an AS2Model if possible.
        """
        match value:
            case dict():
                # Note: We might want a more sophisticated lookup for the right class here
                return AS2Model(value)
            case list():
                return [self._wrap_value(v) for v in value]
            case _:
                return value

    def _resolve_uri(self, uri: str) -> str:
        """
        Placeholder for URI resolution logic.
        """
        return uri

    def to_dict(self) -> Dict[str, Any]:
        # SnapletBase.to_dict handles recursion for nested Snaplet objects in _cache
        return super().to_dict()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} type={self._data.get('type')}>"
