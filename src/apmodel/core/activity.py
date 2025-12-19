from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from pydantic import Field

from ..vocab.actor import Actor
from .object import Object

if TYPE_CHECKING:
    from ..vocab.activity.accept import Accept
    from ..vocab.activity.reject import Reject
    from ..vocab.actor import Actor


class Activity(Object):
    type: Optional[str] = Field(default="Activity", kw_only=True, frozen=True)
    actor: Optional["str | Actor | List[str | Actor]"] = Field(default=None)
    object: Optional[str | Object] = Field(default=None)
    target: Optional["str | Actor | List[str | Actor]"] = Field(
        default=None
    )
    result: Optional[dict] = Field(default=None)
    origin: Optional[dict] = Field(default=None)
    instrument: Optional[dict] = Field(default=None)

    def accept(self, id: str, actor: Actor) -> "Accept":
        from ..vocab.activity.accept import Accept

        return Accept(id=id, object=self, actor=actor)

    def reject(self, id: str, actor: Actor) -> "Reject":
        from ..vocab.activity.reject import Reject

        return Reject(id=id, object=self, actor=actor)

    def dump(self, id_only: bool = True, **kwargs) -> dict:
        """Export activity to JSON

        Args:
            id_only (bool, optional): Don't convert to url for target, actor. Defaults to False.

        Returns:
            _type_: _description_
        """
        out = super().dump()
        if not id_only:
            actor = out.get("actor")
            if isinstance(actor, dict):
                out["actor"] = actor.get("id")
            elif isinstance(actor, list):
                out["actor"] = [
                    item.get("id") if isinstance(item, dict) else item
                    for item in actor
                ]
            if isinstance(out.get("object"), dict):
                out["object"] = out["object"]["id"]
        return out


class IntransitiveActivity(Activity):
    type: Optional[str] = Field(default="IntransitiveActivity", kw_only=True, frozen=True)

    def accept(self, id: str, actor: Actor) -> "Accept":
        from ..vocab.activity.accept import Accept

        return Accept(id=id, object=self, actor=actor)

    def reject(self, id: str, actor: Actor) -> "Reject":
        from ..vocab.activity.reject import Reject

        return Reject(id=id, object=self, actor=actor)
