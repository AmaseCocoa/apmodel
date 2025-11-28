from typing import Any, Dict, List, Optional, Union

from pydantic import Field, model_serializer

from ..context import LDContext
from ..core.collection import Collection, OrderedCollection
from ..core.object import Object
from ..extra.cid import Multikey
from ..extra.security import CryptographicKey


class ActorEndpoints(Object):
    type: Optional[str] = Field(
        default="as:Endpoints", kw_only=True, frozen=True
    )
    sharedInbox: Optional[Union[str, OrderedCollection]] = Field(default=None)


class Actor(Object):
    inbox: Optional[Union[str, OrderedCollection]] = Field(default=None)
    outbox: Optional[Union[str, OrderedCollection]] = Field(default=None)
    followers: Optional[Union[str, OrderedCollection, Collection]] = Field(
        default=None
    )
    following: Optional[Union[str, OrderedCollection, Collection]] = Field(
        default=None
    )
    liked: Optional[Union[str, OrderedCollection, Collection]] = Field(
        default=None
    )
    streams: Optional[Union[str, Collection]] = Field(default=None)
    preferredUsername: Optional[str] = Field(default=None)
    endpoints: Optional[ActorEndpoints] = Field(default=None)
    discoverable: Optional[bool] = Field(default=None)
    indexable: Optional[bool] = Field(default=None)
    suspended: Optional[bool] = Field(default=None)
    memorial: Optional[bool] = Field(default=None)
    publicKey: Optional[CryptographicKey] = Field(default=None)
    assertionMethod: List[Multikey] = Field(default_factory=list)

    @model_serializer(when_used="always")
    def custom_to_json(self) -> Dict[str, Any]:
        result = self.model_dump(by_alias=False, mode="json", exclude_none=True)

        dynamic_context = LDContext(result.get("@context", []))

        if result.get("publicKey"):
            dynamic_context.add("https://w3id.org/security/v1")
        if result.get("assertionMethod"):
            dynamic_context.add("https://w3id.org/did/v1")

        if result.get("manuallyApprovesFollowers"):
            dynamic_context.add(
                {"manuallyApprovesFollowers": "as:manuallyApprovesFollowers"}
            )
        if result.get("sensitive"):
            dynamic_context.add({"sensitive": "as:sensitive"})

        toot_context = {"toot": "http://joinmastodon.org/ns#"}

        if result.get("featured"):
            dynamic_context.add({**toot_context, "featured": "toot:featured"})
        if result.get("featuredTags"):
            dynamic_context.add(
                {**toot_context, "featuredTags": "toot:featuredTags"}
            )
        if result.get("indexable"):
            dynamic_context.add({**toot_context, "indexable": "toot:indexable"})
        if result.get("discoverable"):
            dynamic_context.add(
                {**toot_context, "discoverable": "toot:discoverable"}
            )
        if result.get("suspended"):
            dynamic_context.add({**toot_context, "suspended": "toot:suspended"})
        if result.get("memorial"):
            dynamic_context.add({**toot_context, "memorial": "toot:memorial"})

        if any(
            isinstance(item, dict) and item.get("type") == "PropertyValue"
            for item in result.get("attachment", [])
        ):
            dynamic_context.add(
                {
                    "schema": "http://schema.org#",
                    "value": "schema:value",
                    "PropertyValue": "schema:PropertyValue",
                }
            )

        if any(
            isinstance(item, dict) and item.get("type") == "Emoji"
            for item in result.get("tag", [])
        ):
            dynamic_context.add({**toot_context, "Emoji": "toot:Emoji"})

        if any(
            isinstance(item, dict) and item.get("type") == "Hashtag"
            for item in result.get("tag", [])
        ):
            dynamic_context.add(
                {"Hashtag": "https://www.w3.org/ns/activitystreams#Hashtag"}
            )

        final_context = dynamic_context.full_context
        if final_context:
            result["@context"] = final_context

        return result


class Application(Actor):
    type: Optional[str] = Field(default="Application", kw_only=True, frozen=True)


class Group(Actor):
    type: Optional[str] = Field(default="Group", kw_only=True, frozen=True)


class Organization(Actor):
    type: Optional[str] = Field(default="Organization", kw_only=True, frozen=True)


class Person(Actor):
    type: Optional[str] = Field(default="Person", kw_only=True, frozen=True)


class Service(Actor):
    type: Optional[str] = Field(default="Service", kw_only=True, frozen=True)
