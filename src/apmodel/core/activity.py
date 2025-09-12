from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, List, Union

from ..types import Undefined
from ..vocab.actor import Actor
from .object import Object

if TYPE_CHECKING:
    from ..vocab.activity.accept import Accept
    from ..vocab.activity.reject import Reject
    from ..vocab.actor import Actor


@dataclass
class Activity(Object):
    type: Union[str, Undefined] = field(default="Activity", kw_only=True)
    actor: Union[str, "Actor", List[Union[str, "Actor"]], Undefined] = field(
        default_factory=Undefined
    )
    object: Union[str, Object, Undefined] = field(default_factory=Undefined)
    target: Union[str, "Actor", List[Union[str, "Actor"]], Undefined] = field(
        default_factory=Undefined
    )
    result: Union[dict, Undefined] = field(default_factory=Undefined)
    origin: Union[dict, Undefined] = field(default_factory=Undefined)
    instrument: Union[dict, Undefined] = field(default_factory=Undefined)

    def accept(self, id: str, actor: Actor) -> "Accept":
        from ..vocab.activity.accept import Accept

        return Accept(id=id, object=self, actor=actor)

    def reject(self, id: str, actor: Actor) -> "Reject":
        from ..vocab.activity.reject import Reject

        return Reject(id=id, object=self, actor=actor)
    
    def to_json(self, keep_object: bool = False): # pyright: ignore[reportIncompatibleMethodOverride]
        """Export activity to JSON

        Args:
            keep_object (bool, optional): Don't convert to url for target,actor. Defaults to False.

        Returns:
            _type_: _description_
        """
        if not keep_object:
            if isinstance(self.actor, Actor):
                self.actor = self.actor.id
            if isinstance(self.object, Object):
                self.object = self.object.id

        return super().to_json()

    

@dataclass
class IntransitiveActivity(Activity):
    type: Union[str, Undefined] = field(default="IntransitiveActivity", kw_only=True)

    def accept(self, id: str, actor: Actor) -> "Accept":
        from ..vocab.activity.accept import Accept

        return Accept(id=id, object=self, actor=actor)

    def reject(self, id: str, actor: Actor) -> "Reject":
        from ..vocab.activity.reject import Reject

        return Reject(id=id, object=self, actor=actor)
