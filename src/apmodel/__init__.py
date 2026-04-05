from apmodel.loader import load

__all__ = ["load"]


def _rebuild_models() -> None:
    """Rebuild all models to resolve forward references."""
    import sys

    from apmodel.base import AS2Model
    from apmodel.inference import generate_type_ns

    # Import all model modules to ensure they are registered
    from apmodel import (
        core,
        wrapper,
    )
    from apmodel.objects import (
        actor,
        article,
        document,
        event,
        hashtag,
        mention,
        note,
        place,
        profile,
        relationship,
        tombstone,
    )
    from apmodel.activity import (
        accept,
        add,
        announce,
        arrive,
        block,
        create,
        delete,
        dislike,
        flag,
        follow,
        ignore,
        invite,
        join,
        leave,
        like,
        listen,
        move,
        offer,
        question,
        read,
        reject,
        remove,
        travel,
        undo,
        update,
        view,
    )

    # Rebuild all AS2Model subclasses
    type_ns = generate_type_ns()
    for name, obj in sys.modules.copy().items():
        if "apmodel" in name:
            mod = sys.modules.get(name)
            if mod:
                for attr_name in dir(mod):
                    attr = getattr(mod, attr_name, None)
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, AS2Model)
                        and attr is not AS2Model
                    ):
                        attr.model_rebuild(_types_namespace=type_ns)


_rebuild_models()
