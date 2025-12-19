import warnings
from typing import Any, Dict, Optional, TypeVar, Unpack

from pydantic import (
    BaseModel,
    ConfigDict,
    model_serializer,
    model_validator,
)
from pydantic.alias_generators import to_camel

from ._core._initial._registory import _registory as __registory
from .context import LDContext

T = TypeVar("T", bound="ActivityPubModel")


class ActivityPubModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, serialize_by_alias=True, extra="allow")

    def __post_init__(self):
        if hasattr(self, "context"):
            self.context = LDContext(self.context)

    @model_validator(mode="before")
    @classmethod
    def validate_secret(cls, d: Any) -> LDContext | Any:
        if hasattr(cls, "context"):
            return LDContext(d)
        return d

    def dump(self, **kwargs) -> dict:
        out = super().model_dump(exclude_none=True, **kwargs)
        return out

    @model_serializer(when_used="json")
    def serialize_to_json_ld(self) -> Dict[str, Any]:
        aggregated_context: Optional[LDContext]
        try:
            aggregated_context = self.context + LDContext()
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
                    if hasattr(value, "context") and value.context:
                        aggregated_context = aggregated_context + value.context

                    child_json.pop("@context", None)
                data[field_name] = child_json

            elif isinstance(value, list):
                processed_list = []
                for item in value:
                    if isinstance(item, ActivityPubModel):
                        child_json = item.serialize_to_json_ld()

                        if aggregated_context:
                            if hasattr(item, "context") and item.context:
                                aggregated_context = (
                                    aggregated_context + item.context
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

        return data

    def __init_subclass__(cls, **kwargs: Unpack[ConfigDict]):
        model_type = getattr(cls, "_model_type", None)
        if model_type:
            if model_type in __registory:
                existing_cls = __registory[model_type]
                from apmodel.core.activity import Activity, IntransitiveActivity
                from apmodel.core.collection import (
                    Collection,
                    CollectionPage,
                    OrderedCollection,
                    OrderedCollectionPage,
                )
                from apmodel.core.link import Link
                from apmodel.core.object import Object

                if issubclass(cls, existing_cls) and existing_cls not in [
                    Object,
                    Link,
                    Activity,
                    Collection,
                    CollectionPage,
                    OrderedCollection,
                    OrderedCollectionPage,
                    IntransitiveActivity,
                ]:  # cls can't override if existing_cls is in base models
                    __registory[model_type] = cls
                    return
                else:
                    warnings.warn(
                        f"Model type '{model_type}' for class {cls.__name__} conflicts with "
                        f"existing model {existing_cls.__name__}. Registration skipped due to "
                        f"missing inheritance relationship (Must inherit from {existing_cls.__name__}).",
                        UserWarning,
                        stacklevel=2,
                    )
        return super().__init_subclass__(**kwargs)
