from __future__ import annotations

from pydantic import Field
from typing import Union, List

from .object import Object
from .link import Link
from ..types import Undefined


class Collection(Object):
    type: Union[str, Undefined] = Field(default="Collection", kw_only=True)

    totalItems: Union[int, Undefined] = Field(default_factory=Undefined)
    current: Union[str, dict, Link, Undefined] = Field(default_factory=Undefined)
    first: Union[str, dict, Link, Undefined] = Field(default_factory=Undefined)
    last: Union[str, dict, Link, Undefined] = Field(default_factory=Undefined)
    items: Union[List[Union[Object, Link]], Undefined] = Field(default_factory=Undefined)
    orderedItems: Union[List[Union[Object, Link]], Undefined] = Field(default_factory=Undefined)

    def __post_init__(self):
        if isinstance(self.totalItems, int) and self.totalItems < 0:
            raise ValueError("totalItems must be non-negative integer.")


class CollectionPage(Collection):
    type: Union[str, Undefined] = Field(default="CollectionPage", kw_only=True)

    partOf: Union[str, Collection, Link, Undefined] = Field(default_factory=Undefined)

    next: Union[str, CollectionPage, Link, Undefined] = Field(default_factory=Undefined)
    prev: Union[str, CollectionPage, Link, Undefined] = Field(default_factory=Undefined)


class OrderedCollection(Collection):
    type: Union[str, Undefined] = Field(default="OrderedCollection", kw_only=True)


class OrderedCollectionPage(CollectionPage):
    type: Union[str, Undefined] = Field(default="OrderedCollectionPage", kw_only=True)

    startIndex: Union[int, Undefined] = Field(default_factory=Undefined)
    
    def __post_init__(self):
        if isinstance(self.startIndex, int) and self.startIndex < 0:
            raise ValueError("startIndex must be non-negative integer.")