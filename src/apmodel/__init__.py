from __future__ import annotations

from apmodel.base import AS2Model, to_dict
from apmodel.loader import load
from apmodel.inference import TypeInferencer

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

from apmodel.cid import DataIntegrityProof, Multikey
from apmodel.context import Context
from apmodel.enums import Visibility
from apmodel.litepub import EmojiReact
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
    import importlib.util
    
    from apmodel.inference import generate_type_ns

    type_ns = generate_type_ns()

    model_classes = {
"CryptographicKey": "apmodel.security.CryptographicKey","EmojiReact": "apmodel.litepub.EmojiReact","Context": "apmodel.context.Context","TypeInferencer": "apmodel.inference.TypeInferencer","DataIntegrityProof": "apmodel.cid.DataIntegrityProof","Multikey": "apmodel.cid.Multikey","Emoji": "apmodel.mastodon.Emoji","Activity": "apmodel.core.Activity","Collection": "apmodel.core.Collection","CollectionPage": "apmodel.core.CollectionPage","IntransitiveActivity": "apmodel.core.IntransitiveActivity","Link": "apmodel.core.Link","Object": "apmodel.core.Object","OrderedCollection": "apmodel.core.OrderedCollection","OrderedCollectionPage": "apmodel.core.OrderedCollectionPage","Visibility": "apmodel.enums.Visibility","PropertyValue": "apmodel.schema.PropertyValue","AS2Model": "apmodel.base.AS2Model","Nodeinfo": "apmodel.nodeinfo.Nodeinfo","NodeinfoServices": "apmodel.nodeinfo.NodeinfoServices","NodeinfoSoftware": "apmodel.nodeinfo.NodeinfoSoftware","NodeinfoUsage": "apmodel.nodeinfo.NodeinfoUsage","NodeinfoUsageUsers": "apmodel.nodeinfo.NodeinfoUsageUsers","Audio": "apmodel.objects.Audio","Document": "apmodel.objects.Document","Image": "apmodel.objects.Image","Page": "apmodel.objects.Page","Video": "apmodel.objects.Video","Place": "apmodel.objects.Place","Event": "apmodel.objects.Event","Tombstone": "apmodel.objects.Tombstone","Profile": "apmodel.objects.Profile","Hashtag": "apmodel.objects.Hashtag","Mention": "apmodel.objects.Mention","Article": "apmodel.objects.Article","Relationship": "apmodel.objects.Relationship","Note": "apmodel.objects.Note","Actor": "apmodel.objects.Actor","ActorEndpoints": "apmodel.objects.ActorEndpoints","Application": "apmodel.objects.Application","Group": "apmodel.objects.Group","Organization": "apmodel.objects.Organization","Person": "apmodel.objects.Person","Service": "apmodel.objects.Service","Undo": "apmodel.activity.Undo","Join": "apmodel.activity.Join","Announce": "apmodel.activity.Announce","Create": "apmodel.activity.Create","Delete": "apmodel.activity.Delete","Question": "apmodel.activity.Question","Dislike": "apmodel.activity.Dislike","Arrive": "apmodel.activity.Arrive","View": "apmodel.activity.View","Block": "apmodel.activity.Block","Invite": "apmodel.activity.Invite","Leave": "apmodel.activity.Leave","Listen": "apmodel.activity.Listen","Flag": "apmodel.activity.Flag","Read": "apmodel.activity.Read","Offer": "apmodel.activity.Offer","Travel": "apmodel.activity.Travel","Move": "apmodel.activity.Move","Like": "apmodel.activity.Like","Remove": "apmodel.activity.Remove","Ignore": "apmodel.activity.Ignore","Update": "apmodel.activity.Update","Follow": "apmodel.activity.Follow","Accept": "apmodel.activity.Accept","TentativeAccept": "apmodel.activity.TentativeAccept","Add": "apmodel.activity.Add","Reject": "apmodel.activity.Reject","TentativeReject": "apmodel.activity.TentativeReject",
    }

    for _, full_path in model_classes.items():
        parts = full_path.rsplit(".", 1)
        if len(parts) != 2:
            continue
    
        mod_name, attr_name = parts
        
        if importlib.util.find_spec(mod_name):
            mod = __import__(mod_name, fromlist=[attr_name])
            if hasattr(mod, attr_name):
                cls = getattr(mod, attr_name)
                
                if isinstance(cls, type) and issubclass(cls, AS2Model):
                    cls.model_rebuild(_types_namespace=type_ns)



_rebuild_models()