import builtins
import datetime
from collections.abc import Callable
from typing import Annotated, Any, Literal, TypeAlias, TypeVar

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PlainSerializer,
    PrivateAttr,
)
from pydantic.main import IncEx
from pydantic.alias_generators import to_camel

from apmodel.context import Context

T = TypeVar("T", bound="AS2Model")


def parse_datetime(v: Any) -> datetime.datetime:  # noqa: ANN401
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

    def model_dump(
        self,
        *,
        mode: Literal["json", "python"] | str = "json",  # noqa: PYI051
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        context: Any | None = None,  # noqa: ANN401
        by_alias: bool | None = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
        exclude_computed_fields: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal["none", "warn", "error"] = True,
        fallback: Callable[[Any], Any] | None = None,
        serialize_as_any: bool = True,
    ) -> dict[str, Any]:

        result = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=True,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            exclude_computed_fields=exclude_computed_fields,
            round_trip=round_trip,
            warnings=warnings,
            fallback=fallback,
            serialize_as_any=serialize_as_any,
        )

        all_contexts = ["https://www.w3.org/ns/activitystreams"]

        def collect_contexts(value: AS2Model | dict | list | tuple | set, visited: set[int]) -> None:
            from apmodel.core import Object

            if isinstance(value, AS2Model):
                value_id = id(value)
                if value_id in visited:
                    return
                visited.add(value_id)

                if getattr(value, "ctx", None) is not None:
                    self._append_unique_context_items(all_contexts, value.ctx)
                if isinstance(value, Object) and getattr(value, "context", None) and isinstance(value.context, str):
                    self._append_unique_context_items(all_contexts, value.context)
                    
                for field_name in value.__class__.model_fields:
                    collect_contexts(getattr(value, field_name), visited)
                if value.model_extra:
                    for extra_value in value.model_extra.values():
                        collect_contexts(extra_value, visited)
            elif isinstance(value, dict):
                if "@context" in value and value["@context"] is not None:
                    self._append_unique_context_items(all_contexts, value["@context"])
                for sub_value in value.values():
                    collect_contexts(sub_value, visited)
            elif isinstance(value, list | tuple | set):
                for item in value:
                    collect_contexts(item, visited)

        collect_contexts(self, set())

        def remove_all_nested_context(obj_dict: dict | list, *, is_root: bool = False):
            if isinstance(obj_dict, dict):
                if not is_root and "@context" in obj_dict:
                    del obj_dict["@context"]
                for v in obj_dict.values():
                    remove_all_nested_context(v, is_root=False)
            elif isinstance(obj_dict, list):
                for item in obj_dict:
                    remove_all_nested_context(item, is_root=False)

        remove_all_nested_context(result, is_root=True)

        result["@context"] = all_contexts
        return result

    def dict(self, **kwargs: Any) -> dict:
        return self.model_dump(**kwargs)

    def dump(self, **kwargs: Any) -> builtins.dict:
        return self.model_dump(**kwargs)


def to_dict(model: AS2Model, *args: Any, **kwargs: Any) -> dict:
    """Convert an AS2Model to a dictionary with proper serialization."""
    return model.model_dump(*args, **kwargs)
