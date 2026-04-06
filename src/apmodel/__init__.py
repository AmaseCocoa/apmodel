from __future__ import annotations

from apmodel.base import AS2Model, to_dict
from apmodel.cid import DataIntegrityProof, Multikey
from apmodel.context import Context
from apmodel.core import (
    Activity,
    Collection,
    CollectionPage,
    IntransitiveActivity,
    Link,
    Object,
    OrderedCollection,
    OrderedCollectionPage,
)
from apmodel.enums import Visibility
from apmodel.inference import TypeInferencer
from apmodel.litepub import EmojiReact
from apmodel.loader import load
from apmodel.mastodon import Emoji
from apmodel.schema import PropertyValue
from apmodel.security import CryptographicKey

__all__ = [
    "load",
    "to_dict",
    "AS2Model",
    "TypeInferencer",
    "Activity",
    "Collection",
    "CollectionPage",
    "IntransitiveActivity",
    "Link",
    "Object",
    "OrderedCollection",
    "OrderedCollectionPage",
    "DataIntegrityProof",
    "Multikey",
    "Context",
    "Visibility",
    "EmojiReact",
    "Emoji",
    "PropertyValue",
    "CryptographicKey",
]


def _rebuild_models() -> None:
    """Rebuild all models to resolve forward references."""
    import sys

    from apmodel.inference import generate_type_ns

    type_ns = generate_type_ns()

    model_classes = {
        "Audio": "apmodel.objects.Audio",
        "Document": "apmodel.objects.Document",
        "Image": "apmodel.objects.Image",
        "Page": "apmodel.objects.Page",
        "Video": "apmodel.objects.Video",
        "Place": "apmodel.objects.Place",
        "Event": "apmodel.objects.Event",
        "Tombstone": "apmodel.objects.Tombstone",
        "Profile": "apmodel.objects.Profile",
        "Hashtag": "apmodel.objects.Hashtag",
        "Mention": "apmodel.objects.Mention",
        "Article": "apmodel.objects.Article",
        "Relationship": "apmodel.objects.Relationship",
        "Note": "apmodel.objects.Note",
        "Actor": "apmodel.objects.Actor",
        "ActorEndpoints": "apmodel.objects.ActorEndpoints",
        "Application": "apmodel.objects.Application",
        "Group": "apmodel.objects.Group",
        "Organization": "apmodel.objects.Organization",
        "Person": "apmodel.objects.Person",
        "Service": "apmodel.objects.Service",
        "Undo": "apmodel.activity.Undo",
        "Join": "apmodel.activity.Join",
        "Announce": "apmodel.activity.Announce",
        "Create": "apmodel.activity.Create",
        "Delete": "apmodel.activity.Delete",
        "Question": "apmodel.activity.Question",
        "Dislike": "apmodel.activity.Dislike",
        "Arrive": "apmodel.activity.Arrive",
        "View": "apmodel.activity.View",
        "Block": "apmodel.activity.Block",
        "Invite": "apmodel.activity.Invite",
        "Leave": "apmodel.activity.Leave",
        "Listen": "apmodel.activity.Listen",
        "Flag": "apmodel.activity.Flag",
        "Read": "apmodel.activity.Read",
        "Offer": "apmodel.activity.Offer",
        "Travel": "apmodel.activity.Travel",
        "Move": "apmodel.activity.Move",
        "Like": "apmodel.activity.Like",
        "Remove": "apmodel.activity.Remove",
        "Ignore": "apmodel.activity.Ignore",
        "Update": "apmodel.activity.Update",
        "Follow": "apmodel.activity.Follow",
        "Accept": "apmodel.activity.Accept",
        "TentativeAccept": "apmodel.activity.TentativeAccept",
        "Add": "apmodel.activity.Add",
        "Reject": "apmodel.activity.Reject",
        "TentativeReject": "apmodel.activity.TentativeReject",
        "TinyJLDLoader": "apmodel._vendor.tinyjld.TinyJLDLoader",
        "TinyJLD": "apmodel._vendor.tinyjld.TinyJLD",
    }

    for cls_name, full_path in model_classes.items():
        try:
            parts = full_path.rsplit(".", 1)
            if len(parts) == 2:
                mod_name, attr_name = parts
                mod = __import__(mod_name, fromlist=[attr_name])
                cls = getattr(mod, attr_name, None)
                if cls is not None and isinstance(cls, type) and issubclass(cls, AS2Model):
                    cls.model_rebuild(_types_namespace=type_ns)
        except Exception:
            pass


_rebuild_models()
