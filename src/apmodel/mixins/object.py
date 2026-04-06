from typing import Any, Protocol

from pydantic import ValidationError, ValidationInfo, field_validator


class ObjectFieldsProtocol(Protocol):
    """Protocol for Object fields that need validation."""

    attachment: Any
    tag: Any
    replies: Any


class ObjectMixin:
    """Mixin for Object to add field validators for type inference."""

    @field_validator("attachment", "tag", mode="before")
    @classmethod
    def infer_and_load_attachment_types(cls, v: Any, info: ValidationInfo):  # noqa: ANN206,ANN401
        """Try to infer the correct AS2 type for dict items in the attachment field."""
        if not isinstance(v, list):
            v = [v] if v else []

        if not info.context:
            return v

        result = []
        context = info.context
        for item in v:
            if isinstance(item, dict):
                try:
                    from apmodel.loader import type_loader

                    item_with_context = dict(item)
                    if "@context" not in item_with_context:
                        item_with_context["@context"] = context.get("@context", context)

                    model_cls = type_loader.infer(item_with_context, parent_context=context)
                    if model_cls:
                        loaded = model_cls.model_validate(item_with_context, context=context)
                        result.append(loaded)
                    else:
                        result.append(item)
                except (ValidationError, ImportError, AttributeError, TypeError):
                    result.append(item)
            else:
                result.append(item)

        return result

    @field_validator("replies", mode="before")
    @classmethod
    def infer_and_load_single_object(cls, v: Any, info: ValidationInfo):  # noqa: ANN206,ANN401
        """Try to infer the correct AS2 type for dict items in object-type fields."""
        if not isinstance(v, dict):
            return v

        if not info.context:
            return v

        context = info.context

        item_type = v.get("type")
        if not item_type:
            return v

        try:
            from apmodel.loader import type_loader

            item_with_context = dict(v)
            if "@context" not in item_with_context:
                item_with_context["@context"] = context.get("@context", context)

            model_cls = type_loader.infer(item_with_context, parent_context=context)
            if model_cls:
                loaded = model_cls.model_validate(item_with_context, context=context)
                return loaded
            else:
                return v
        except (ValidationError, ImportError, AttributeError, TypeError):
            return v
