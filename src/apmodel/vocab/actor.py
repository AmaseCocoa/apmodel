from typing import Any, ClassVar, Dict, List, Optional

from pydantic import Field

from ..context import LDContext
from ..core.collection import Collection, OrderedCollection
from ..core.object import Object
from ..extra.cid import Multikey
from ..extra.security import CryptographicKey


class ActorEndpoints(Object):
    _model_type: ClassVar[str] = "__apmodel_exclude__"

    type: Optional[str] = Field(
        default="as:Endpoints", kw_only=True, frozen=True
    )
    shared_inbox: Optional[str | OrderedCollection] = Field(default=None)


class Actor(Object):
    _model_type: ClassVar[str] = "__apmodel_exclude__"

    inbox: Optional[str | OrderedCollection] = Field(default=None)
    outbox: Optional[str | OrderedCollection] = Field(default=None)
    followers: Optional[str | OrderedCollection | Collection] = Field(
        default=None
    )
    following: Optional[str | OrderedCollection | Collection] = Field(
        default=None
    )
    liked: Optional[str | OrderedCollection | Collection] = Field(
        default=None
    )
    streams: Optional[str | Collection] = Field(default=None)
    preferred_username: Optional[str] = Field(default=None)
    endpoints: Optional[ActorEndpoints] = Field(default=None)
    discoverable: Optional[bool] = Field(default=None)
    indexable: Optional[bool] = Field(default=None)
    suspended: Optional[bool] = Field(default=None)
    memorial: Optional[bool] = Field(default=None)
    public_key: Optional[CryptographicKey] = Field(default=None)
    assertion_method: List[Multikey] = Field(default_factory=list)

    def _inference_context(self, result: dict) -> Dict[str, Any]:
        res_ctx = result.get("@context", [])
        dynamic_context = LDContext(res_ctx)
        dynamic_context.add("https://www.w3.org/ns/activitystreams")

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

        tootcontext = {"toot": "http://joinmastodon.org/ns#"}

        if result.get("featured"):
            dynamic_context.add({**tootcontext, "featured": "toot:featured"})
        if result.get("featuredTags"):
            dynamic_context.add(
                {**tootcontext, "featuredTags": "toot:featuredTags"}
            )
        if result.get("indexable"):
            dynamic_context.add({**tootcontext, "indexable": "toot:indexable"})
        if result.get("discoverable"):
            dynamic_context.add(
                {**tootcontext, "discoverable": "toot:discoverable"}
            )
        if result.get("suspended"):
            dynamic_context.add({**tootcontext, "suspended": "toot:suspended"})
        if result.get("memorial"):
            dynamic_context.add({**tootcontext, "memorial": "toot:memorial"})

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
            dynamic_context.add({**tootcontext, "Emoji": "toot:Emoji"})

        if any(
            isinstance(item, dict) and item.get("type") == "Hashtag"
            for item in result.get("tag", [])
        ):
            dynamic_context.add(
                {"Hashtag": "https://www.w3.org/ns/activitystreams#Hashtag"}
            )

        finalcontext = dynamic_context.full_context
        if finalcontext:
            result["@context"] = finalcontext

        return result


class Application(Actor):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Application"
    type: Optional[str] = Field(
        default="Application", kw_only=True, frozen=True
    )


class Group(Actor):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Group"
    type: Optional[str] = Field(default="Group", kw_only=True, frozen=True)


class Organization(Actor):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Organization"
    type: Optional[str] = Field(
        default="Organization", kw_only=True, frozen=True
    )


class Person(Actor):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Person"
    type: Optional[str] = Field(default="Person", kw_only=True, frozen=True)


class Service(Actor):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Service"
    type: Optional[str] = Field(default="Service", kw_only=True, frozen=True)
