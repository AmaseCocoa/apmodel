from __future__ import annotations

from typing import List, Optional, Union

from pydantic import Field

from .link import Link
from .object import Object


class Collection(Object):
    type: Optional[str] = Field(default="Collection", kw_only=True)

    totalItems: Optional[int] = Field(default=None, ge=0)
    current: Optional[Union[str, dict, Link]] = Field(default=None)
    first: Optional[Union[str, dict, Link]] = Field(default=None)
    last: Optional[Union[str, dict, Link]] = Field(default=None)
    items: Optional[List[Union[Object, Link]]] = Field(default=None)
    orderedItems: Optional[List[Union[Object, Link]]] = Field(default=None)


class CollectionPage(Collection):
    type: Optional[str] = Field(default="CollectionPage", kw_only=True)

    partOf: Optional[Union[str, Collection, Link]] = Field(default=None)

    next: Optional[Union[str, CollectionPage, Link]] = Field(default=None)
    prev: Optional[Union[str, CollectionPage, Link]] = Field(default=None)


class OrderedCollection(Collection):
    type: Optional[str] = Field(default="OrderedCollection", kw_only=True)


class OrderedCollectionPage(CollectionPage):
    type: Optional[str] = Field(default="OrderedCollectionPage", kw_only=True)

    startIndex: Optional[int] = Field(default=None, ge=0)
