import datetime
from typing import Annotated, Any, TypeAlias, TypeVar

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PlainSerializer,
    PrivateAttr,
)

from apmodel.context import Context

T = TypeVar("T", bound="AS2Model")


def parse_datetime(v: Any) -> datetime.datetime: # noqa: ANN401
    """Parse a datetime value, converting ISO 8601 strings to datetime objects."""
    if isinstance(v, str):
        # Parse ISO 8601 datetime string
        if v.endswith("Z"):
            v = v[:-1] + "+00:00"
        return datetime.datetime.fromisoformat(v)
    return v


ZDateTime: TypeAlias = Annotated[
    datetime.datetime | str,
    BeforeValidator(parse_datetime),
    PlainSerializer(lambda v: (v if v.tzinfo else v.replace(tzinfo=datetime.timezone.utc)).astimezone(datetime.timezone.utc).isoformat().replace("+00:00", "Z")),
]

# Plain datetime string type - accepts datetime or string, no parsing
PlainDateTime: TypeAlias = datetime.datetime | str


def to_camel(string: str) -> str:
    words = string.split("_")
    # First word stays lowercase, subsequent words are capitalized
    return words[0] + "".join(word.capitalize() for word in words[1:])


class AS2Model(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="allow",
        defer_build=True,
    )
    _is_rebuilt: bool = PrivateAttr(default=False)

    ctx: Context | None = Field(alias="@context", kw_only=True, default=None)

    @staticmethod
    def _append_unique_context_items(all_contexts: list[Any], context_data: Any) -> None:  # noqa: ANN401
        parsed = Context.parse(context_data)
        for item in parsed.value:
            if item not in all_contexts:
                all_contexts.append(item)

    def dump(self, *args: Any, **kwargs: Any) -> dict:
        kwargs.setdefault("by_alias", True)
        all_contexts = ["https://www.w3.org/ns/activitystreams"]

        def collect_contexts(value: Any, visited: set[int]) -> None:  # noqa: ANN401
            if isinstance(value, AS2Model):
                value_id = id(value)
                if value_id in visited:
                    return
                visited.add(value_id)

                if value.ctx is not None:
                    self._append_unique_context_items(all_contexts, value.ctx)

                if hasattr(value, "context") and isinstance(value.context, str) and value.context:
                    self._append_unique_context_items(all_contexts, value.context)

                for field_name in value.__class__.model_fields:
                    collect_contexts(getattr(value, field_name), visited)

                if value.model_extra:
                    for extra_value in value.model_extra.values():
                        collect_contexts(extra_value, visited)
                return

            if isinstance(value, dict):
                if "@context" in value and value["@context"] is not None:
                    self._append_unique_context_items(all_contexts, value["@context"])
                for sub_value in value.values():
                    collect_contexts(sub_value, visited)
                return

            if isinstance(value, list | tuple | set):
                for item in value:
                    collect_contexts(item, visited)

        kwargs.setdefault("exclude_none", True)
        kwargs.setdefault("mode", "json")
        kwargs.setdefault("serialize_as_any", True)
        result = self.model_dump(*args, **kwargs)

        collect_contexts(self, set())

        # Remove nested @context from all nested objects
        def remove_all_nested_context(obj_dict: dict, *, is_root: bool | None = None):
            if isinstance(obj_dict, dict):
                if not is_root and "@context" in obj_dict:
                    del obj_dict["@context"]

                for value in obj_dict.values():
                    if isinstance(value, dict):
                        remove_all_nested_context(value, is_root=False)
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                remove_all_nested_context(item, is_root=False)

        remove_all_nested_context(result, is_root=True)

        # Set the combined context as a list
        result["@context"] = all_contexts

        return result


def to_dict(model: AS2Model, *args: Any, **kwargs: Any) -> dict:
    """Convert an AS2Model to a dictionary with proper serialization."""
    return model.dump(*args, **kwargs)
