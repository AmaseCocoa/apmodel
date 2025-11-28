from typing import Any, Dict, Optional, TypeVar

from pydantic import BaseModel, Field, model_serializer, model_validator

from .context import LDContext

T = TypeVar("T", bound="ActivityPubModel")


class ActivityPubModel(BaseModel):
    _extra: dict = Field(default_factory=dict)
    
    
    def __post_init__(self):
        if hasattr(self, "_context"):
            self._context = LDContext(self._context)

    @model_validator(mode="before")
    @classmethod
    def validate_secret(cls, d: Any) -> LDContext | Any:
        if hasattr(cls, "_context"):
            return LDContext(d)
        return d

    def dump(self, **kwargs) -> dict:
        out = super().model_dump(
            exclude_none=True,
            **kwargs
        )
        return out

    @model_serializer(when_used="json")
    def serialize_to_json_ld(self) -> Dict[str, Any]:
        aggregated_context: Optional[LDContext]
        try:
            aggregated_context = self._context + LDContext()
        except AttributeError:
            aggregated_context = None

        data: Dict[str, Any] = {}

        for field_name, field_info in self.__class__.model_fields.items():
            value = getattr(self, field_name)

            if field_name.startswith("_") or not value:
                continue

            if isinstance(value, ActivityPubModel):
                child_json = value.serialize_to_json_ld()

                if aggregated_context:
                    if hasattr(value, "_context") and value._context:
                        aggregated_context = aggregated_context + value._context

                    child_json.pop("@context", None)
                data[field_name] = child_json

            elif isinstance(value, list):
                processed_list = []
                for item in value:
                    if isinstance(item, ActivityPubModel):
                        child_json = item.serialize_to_json_ld()

                        if aggregated_context:
                            if hasattr(item, "_context") and item._context:
                                aggregated_context = (
                                    aggregated_context + item._context
                                )
                            child_json.pop("@context", None)
                        processed_list.append(child_json)
                    else:
                        processed_list.append(item)
                data[field_name] = processed_list

            else:
                data[field_name] = value

        if aggregated_context:
            data["@context"] = aggregated_context.full_context
        if self._extra:
            data.update(self._extra)

        return data