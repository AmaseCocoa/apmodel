from typing import Any

from apmodel.types import ActivityPubModel

from ._core._initial import (
    _rebuild,  # type: ignore # noqa: F401,F811
)
from ._version import __version__, __version_tuple__  # noqa: F401
from .context import LDContext
from .core import (
    Activity,
    Collection,
    CollectionPage,
    Link,
    Object,
    OrderedCollection,
    OrderedCollectionPage,
)
from .loader import load
from .vocab import (
    Application,  # noqa: F401
    Group,  # noqa: F401
    Organization,  # noqa: F401
    Person,
    Service,  # noqa: F401
)


def to_dict(obj: ActivityPubModel) -> dict:
    raw_data = obj.model_dump(by_alias=True, exclude_none=True) # , exclude_defaults=True

    master_context = LDContext()

    def extract_and_clean(data: Any) -> Any:
        if isinstance(data, dict):
            new_dict = {}
            for k, v in data.items():
                if k == "@context":
                    master_context.add(v)
                else:
                    new_dict[k] = extract_and_clean(v)
            return new_dict

        elif isinstance(data, list):
            return [extract_and_clean(item) for item in data]

        return data

    if hasattr(obj, "_inference_context"):
        raw_data = obj._inference_context(raw_data)

    cleaned_result = extract_and_clean(raw_data)

    context_list = master_context.full_context
    if context_list:
        final_ctx = context_list[0] if len(context_list) == 1 else context_list
        return {"@context": final_ctx, **cleaned_result}

    return cleaned_result


__all__ = [
    # Core Types
    "Object",
    "Link",
    "Activity",
    "Collection",
    "OrderedCollection",
    "CollectionPage",
    "OrderedCollectionPage",
    # Actor
    "Person",
    # load / dump
    "load",
    "to_dict",
    # context
    "LDContext",
]
