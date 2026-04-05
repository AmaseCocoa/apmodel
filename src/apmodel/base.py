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

    def dump(self, *args: Any, **kwargs: Any) -> dict:
        # Use by_alias=True to serialize field aliases like @context
        kwargs.setdefault("by_alias", True)
        # First get full dump to collect nested contexts
        full_result = self.model_dump(by_alias=True, serialize_as_any=True, mode="json")

        # Collect all contexts from nested objects
        all_contexts = []

        # Add default ActivityStreams context
        all_contexts.append("https://www.w3.org/ns/activitystreams")

        # Add object's own context if present
        if self.ctx is not None:
            for ctx_item in self.ctx.value:
                if ctx_item not in all_contexts:
                    all_contexts.append(ctx_item)

        # Add the context field if it's a string
        if hasattr(self, "context") and self.context and isinstance(self.context, str) and self.context not in all_contexts:
            all_contexts.append(self.context)

        # Collect contexts from all nested objects recursively
        def collect_all_nested_contexts(obj_dict: dict):
            if isinstance(obj_dict, dict):
                # Collect @context from this object
                if "@context" in obj_dict and obj_dict["@context"] is not None:
                    ctx_val = obj_dict["@context"]
                    if isinstance(ctx_val, str) and ctx_val not in all_contexts:
                        all_contexts.append(ctx_val)
                    elif isinstance(ctx_val, dict):
                        if ctx_val not in all_contexts:
                            all_contexts.append(ctx_val)
                    elif isinstance(ctx_val, list):
                        for item in ctx_val:
                            if item not in all_contexts:
                                all_contexts.append(item)

                # Recursively check all nested objects
                for _, value in obj_dict.items():
                    if isinstance(value, dict):
                        collect_all_nested_contexts(value)
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                collect_all_nested_contexts(item)

        # Collect from full_result but skip the root @context (we already have it)
        for key, value in full_result.items():
            if key != "@context":
                if isinstance(value, dict):
                    collect_all_nested_contexts(value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            collect_all_nested_contexts(item)

        # Now get the result with exclude_none
        kwargs.setdefault("exclude_none", True)
        kwargs.setdefault("mode", "json")
        kwargs.setdefault("serialize_as_any", True)
        result = self.model_dump(*args, **kwargs)

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
