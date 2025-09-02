from dataclasses import dataclass, field
from typing import List, Union

from ..context import LDContext
from ..types import Undefined
from ..core.collection import Collection, OrderedCollection
from ..core.object import Object
from ..extra.schema.propertyvalue import PropertyValue
from ..extra.emoji import Emoji
from ..extra.hashtag import Hashtag

@dataclass
class ActorEndpoints(Object):
    type: Union[str, Undefined] = field(default="as:Endpoints")
    sharedInbox: Union[str, OrderedCollection, Undefined] = field(
        default_factory=Undefined
    )


@dataclass
class Actor(Object):
    inbox: Union[str, OrderedCollection, Undefined] = field(default_factory=Undefined)
    outbox: Union[str, OrderedCollection, Undefined] = field(default_factory=Undefined)
    followers: Union[str, OrderedCollection, Collection, Undefined] = field(
        default_factory=Undefined
    )
    following: Union[str, OrderedCollection, Collection, Undefined] = field(
        default_factory=Undefined
    )
    liked: Union[str, OrderedCollection, Collection, Undefined] = field(
        default_factory=Undefined
    )
    streams: Union[str, Collection, Undefined] = field(default_factory=Undefined)
    preferredUsername: Union[str, Undefined] = field(default_factory=Undefined)
    endpoints: Union[ActorEndpoints, Undefined] = field(default_factory=Undefined)
    attachment: List[Union["Object", PropertyValue]] = field(default_factory=list) # pyright: ignore[reportIncompatibleVariableOverride]
    discoverable: Union[bool, Undefined] = field(default_factory=Undefined)
    indexable: Union[bool, Undefined] = field(default_factory=Undefined)
    suspended: Union[bool, Undefined] = field(default_factory=Undefined)
    memorial: Union[bool, Undefined] = field(default_factory=Undefined)

    def to_json(self):
        context: LDContext = self._context  # type: ignore
        context.add(
            {
                "misskey": "https://misskey-hub.net/ns#",
            }
        )

        result = super().to_json()

        if result.get("publicKey"):
            context.add("https://w3id.org/security/v1")
        if result.get("manuallyApprovesFollowers"):
            context.add({"manuallyApprovesFollowers": "as:manuallyApprovesFollowers"})
        if result.get("sensitive"):
            context.add({"sensitive": "as:sensitive"})
        if result.get("featured"):
            context.add({"toot": "http://joinmastodon.org/ns#", "featured": "toot:featured"})
        if result.get("featuredTags"):
            context.add({"toot": "http://joinmastodon.org/ns#", "featured": "toot:featuredTags"})
        if result.get("indexable"):
            context.add({"toot": "http://joinmastodon.org/ns#", "indexable": "toot:indexable"})
        if result.get("discoverable"):
            context.add({"toot": "http://joinmastodon.org/ns#", "discoverable": "toot:discoverable"})
        if result.get("suspended"):
            context.add({"toot": "http://joinmastodon.org/ns#", "suspended": "toot:suspended"})
        if result.get("memorial"):
            context.add({"toot": "http://joinmastodon.org/ns#", "memorial": "toot:memorial"})
        if any(isinstance(item, PropertyValue) for item in result.get("attachment", [])):
            context.add({"schema": "http://schema.org#", "value": "schema:value", "PropertyValue": "schema:PropertyValue"})
        if any(isinstance(item, Emoji) for item in result.get("tag", [])):
            context.add({"toot": "http://joinmastodon.org/ns#", "memorial": "toot:memorial"})
        if any(isinstance(item, Hashtag) for item in result.get("tag", [])):
            context.add({"Hashtag": "https://www.w3.org/ns/activitystreams#Hashtag"})

        return result


@dataclass
class Application(Actor):
    type: Union[str, Undefined] = field(default="Application")


@dataclass
class Group(Actor):
    type: Union[str, Undefined] = field(default="Group")


@dataclass
class Organization(Actor):
    type: Union[str, Undefined] = field(default="Organization")


@dataclass
class Person(Actor):
    type: Union[str, Undefined] = field(default="Person")


@dataclass
class Service(Actor):
    type: Union[str, Undefined] = field(default="Service")
