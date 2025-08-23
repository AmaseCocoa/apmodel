from typing import Type, TypeVar

T = TypeVar("T", bound="ActivityPubModel")

class Undefined:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Undefined, cls).__new__(cls)
        return cls._instance

    def __repr__(self):
        return 'undefined'

    def __str__(self):
        return 'undefined'
    
class ActivityPubModel:
    @classmethod
    def from_json(cls: Type[T], data: dict) -> T: ...

    def to_json(self) -> dict: ...