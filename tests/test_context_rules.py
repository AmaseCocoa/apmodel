from typing import Any, Literal

from pydantic import Field, model_serializer

from apmodel.base import AS2Model
from apmodel.core import Object
from apmodel.schema import PropertyValue


def test_context_by_field_list_added_when_field_exists():
    value = PropertyValue(name="k", value="v")
    dumped = value.dump()

    assert "http://schema.org#" in dumped["@context"]
    assert {"schema": "http://schema.org#", "value": "schema:value"} in dumped["@context"]


def test_context_by_field_list_not_added_when_field_missing():
    value = PropertyValue(name="k")
    dumped = value.dump()

    assert "http://schema.org#" not in dumped["@context"]
    assert {"schema": "http://schema.org#", "value": "schema:value"} not in dumped["@context"]


def test_context_by_field_list_collected_from_nested_model():
    actor = Object(
        name="actor",
        attachment=[PropertyValue(name="k", value="v")],
    )
    dumped = actor.dump()

    assert "http://schema.org#" in dumped["@context"]
    assert {"schema": "http://schema.org#", "value": "schema:value"} in dumped["@context"]


class WildcardContextModel(AS2Model):
    type: Literal["WildcardContextModel"] = "WildcardContextModel"

    value: str | None = Field(kw_only=True, default=None)
    value_extra: str | None = Field(kw_only=True, default=None)

    @model_serializer(mode='wrap', when_used='always')
    def _serialize_with_conditional_context(self, serializer: Any, info: Any) -> Any:  # noqa: ANN401
        from fnmatch import fnmatchcase
        from apmodel.context import Context
        
        result = serializer(self)
        
        existing_fields = {
            field_name
            for field_name in self.__class__.model_fields
            if getattr(self, field_name, None) is not None
        }
        if self.model_extra:
            existing_fields.update(
                field_name for field_name, value in self.model_extra.items() if value is not None
            )
        
        watched_fields = ["value*"]
        context_data = ["https://example.com/a.jsonld", {"b": "a:b"}]
        
        def field_matches() -> bool:
            if not watched_fields:
                return bool(existing_fields)
            return any(
                fnmatchcase(field_name, pattern)
                for field_name in existing_fields
                for pattern in watched_fields
            )
        
        if field_matches() and context_data:
            conditional = Context.parse(context_data)
            if self.ctx is None:
                self.ctx = conditional
            else:
                self.ctx = self.ctx + conditional
        
        return result


def test_non_standard_context_when_field_exists_supports_wildcard():
    model = WildcardContextModel(value_extra="ok")
    dumped = model.dump()

    assert "https://example.com/a.jsonld" in dumped["@context"]
    assert {"b": "a:b"} in dumped["@context"]
