from dataclasses import dataclass, field
from typing import Union

from ..types import Undefined
from ..core.collection import Collection, OrderedCollection
from ..core.object import Object

@dataclass
class ActorEndpoints(Object):
    type: Union[str, Undefined] = field(default="as:Endpoints")
    sharedInbox: Union[str, OrderedCollection, Undefined] = field(default_factory=Undefined)

@dataclass
class Actor(Object):
    inbox: Union[str, OrderedCollection, Undefined] = field(default_factory=Undefined)
    outbox: Union[str, OrderedCollection, Undefined] = field(default_factory=Undefined)
    followers: Union[str, OrderedCollection, Collection, Undefined] = field(default_factory=Undefined)
    following: Union[str, OrderedCollection, Collection, Undefined] = field(default_factory=Undefined)
    liked: Union[str, OrderedCollection, Collection, Undefined] = field(default_factory=Undefined)
    streams: Union[str, Collection, Undefined] = field(default_factory=Undefined)
    preferredUsername: Union[str, Undefined] = field(default_factory=Undefined)
    preferredUsername: Union[str, Undefined] = field(default_factory=Undefined)
    endpoints: Union[ActorEndpoints, Undefined] = field(default_factory=Undefined)

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