from typing import TYPE_CHECKING, Dict, Optional, Type

from apmodel._core._initial._registry_bootstrap import TYPE_MAPPING

if TYPE_CHECKING:
    from .types import ActivityPubModel


BASE_MODEL_NAMES = {
    "Object",
    "Link",
    "Activity",
    "IntransitiveActivity",
    "Collection",
    "OrderedCollection",
    "CollectionPage",
    "OrderedCollectionPage",
}


class ModelRegistry:
    def __init__(self) -> None:
        self._registry: Dict[str, Type["ActivityPubModel"]] = {
            **TYPE_MAPPING
        }

    def register(self, model_cls: Type["ActivityPubModel"], model_type: str):
        import warnings

        if model_type in self._registry:
            existing_cls = self._registry[model_type]
            if (
                issubclass(model_cls, existing_cls)
                and existing_cls.__name__ not in BASE_MODEL_NAMES
            ):
                self._registry[model_type] = model_cls
            else:
                warnings.warn(
                    f"Model type '{model_type}' for class {model_cls.__name__} conflicts with "
                    f"existing model {existing_cls.__name__}. Registration skipped due to "
                    f"missing inheritance relationship or attempting to override a base model.",
                    UserWarning,
                    stacklevel=2,
                )
        else:
            self._registry[model_type] = model_cls

    def get(self, model_type: str) -> Optional[Type["ActivityPubModel"]]:
        return self._registry.get(model_type)

    def all(self) -> Dict[str, Type["ActivityPubModel"]]:
        return self._registry

    def has(self, model_type: str) -> bool:
        return model_type in self._registry


registry = ModelRegistry()
