from typing import Any, Protocol

from pydantic import ValidationInfo, field_validator


class ObjectFieldsProtocol(Protocol):
    """Protocol for Object fields that need validation."""
    attachment: Any
    tag: Any
    replies: Any


class ObjectMixin:
    """Mixin for Object to add field validators for type inference."""

    @field_validator('attachment', 'tag', mode='before')
    @classmethod
    def infer_and_load_attachment_types(cls, v, info: ValidationInfo):
        """Try to infer the correct AS2 type for dict items in the attachment field."""
        if not isinstance(v, list):
            v = [v] if v else []
        
        # Only try to load if we have context
        if not info.context:
            return v
        
        result = []
        context = info.context
        for item in v:
            if isinstance(item, dict):
                # Try to load with context, but only for known simple types
                try:
                    # Only process if it has a type field we can use
                    item_type = item.get('type')
                    if not item_type:
                        result.append(item)
                        continue
                    
                    # Only load types that are known to not cause hangs
                    loadable_types = ('PropertyValue', 'Emoji', 'Hashtag', 'Document', 'Link', 'Image')
                    if item_type in loadable_types:
                        from apmodel.loader import type_loader
                        # Add parent context to the item if it doesn't have one
                        item_with_context = dict(item)
                        if '@context' not in item_with_context:
                            item_with_context['@context'] = context.get('@context', context)
                        
                        model_cls = type_loader.infer(item_with_context, parent_context=context)
                        if model_cls:
                            loaded = model_cls.model_validate(item_with_context, context=context)
                            result.append(loaded)
                        else:
                            result.append(item)
                    else:
                        # For other types, keep as dict
                        result.append(item)
                except Exception:
                    # If loading fails, keep the dict
                    result.append(item)
            else:
                result.append(item)
        
        return result
    
    @field_validator('replies', mode='before')
    @classmethod
    def infer_and_load_single_object(cls, v, info: ValidationInfo):
        """Try to infer the correct AS2 type for dict items in object-type fields."""
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
