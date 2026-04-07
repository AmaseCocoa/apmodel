from typing import Any, Protocol

from pydantic import ValidationInfo, field_validator


class CollectionFieldsProtocol(Protocol):
    """Protocol for Collection fields that need validation."""
    current: Any
    first: Any
    last: Any


class CollectionMixin:
    """Mixin for Collection to add field validators for type inference."""

    @field_validator('current', 'first', 'last', mode='before')
    @classmethod
    def infer_and_load_collection_field(cls, v, info: ValidationInfo):
        """Try to infer the correct AS2 type for dict items in collection fields."""
        if not isinstance(v, dict):
            return v
        
        # Only try to load if we have context
        if not info.context:
            return v
        
        context = info.context
        
        # Only process if it has a type field we can use
        item_type = v.get('type')
        if not item_type:
            return v
        
        # Try to load
        try:
            from apmodel.loader import type_loader
            # Add parent context to the item if it doesn't have one
            item_with_context = dict(v)
            if '@context' not in item_with_context:
                item_with_context['@context'] = context.get('@context', context)
            
            model_cls = type_loader.infer(item_with_context, parent_context=context)
            if model_cls:
                loaded = model_cls.model_validate(item_with_context, context=context)
                return loaded
            else:
                return v
        except Exception:
            # If loading fails, keep the dict
            return v
