from dataclasses import dataclass, field
import datetime
from typing import Union

from ...types import Undefined
from ...core.activity import IntransitiveActivity
from ...core.object import Object
from ...core.link import Link

@dataclass
class Question(IntransitiveActivity):
    type: Union[str, Undefined] = field(default="Question")
    oneOf: Union[str, Object, Link, Undefined] = field(default_factory=Undefined)
    anyOf: Union[str, Object, Link, Undefined] = field(default_factory=Undefined)
    closed: Union[str, Object, Link, datetime.datetime, bool, Undefined] = field(default_factory=Undefined)

    def __post_init__(self):
        if isinstance(self.closed, str):
            self.closed = datetime.datetime.strptime(self.closed, "%Y-%m-%dT%H:%M:%S")

    def to_json(self):
        closed_old = self.closed
        if isinstance(self.closed, datetime.datetime):
            self.closed = self.closed.strftime("%Y-%m-%dT%H:%M:%S")
        data = super().to_json()
        self.closed = closed_old
        return data