from .core import (
    Object,
    Link,
    Activity,
    IntransitiveActivity,
    Collection,
    OrderedCollection,
    CollectionPage,
    OrderedCollectionPage,
    Actor,
    Image,
    Endpoints
)

_type_map = {
    "Object": Object,
    "Link": Link,
    "Activity": Activity,
    "IntransitiveActivity": IntransitiveActivity,
    "Collection": Collection,
    "OrderedCollection": OrderedCollection,
    "CollectionPage": CollectionPage,
    "OrderedCollectionPage": OrderedCollectionPage,
    "Actor": Actor,
    "Image": Image,
    "Endpoints": Endpoints,
}

def load(data: dict):
    if "type" in data and data["type"] in _type_map:
        cls = _type_map[data["type"]]
        return cls.from_json(data)
    return data
