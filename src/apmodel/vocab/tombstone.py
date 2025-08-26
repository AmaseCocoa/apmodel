import datetime
from dataclasses import dataclass, field
from typing import Union

from ..core.object import Object
from ..types import Undefined

@dataclass
class Tombstone(Object):
    type: Union[str, Undefined] = field(default="Tombstone")
    formerType: str | Object | Undefined = field(default_factory=Undefined)
    deleted: datetime.datetime | str | Undefined = field(default_factory=Undefined)

    def __post_init__(self):
        if isinstance(self.deleted, str):
            self.deleted = datetime.datetime.strptime(self.deleted, "%Y-%m-%dT%H:%M:%S")

    def to_json(self):
        deleted_old = self.deleted
        if isinstance(self.deleted, datetime.datetime):
            self.deleted = self.deleted.strftime("%Y-%m-%dT%H:%M:%S")
        data = super().to_json()
        self.deleted = deleted_old
        return data