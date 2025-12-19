from __future__ import annotations

from typing import List, Optional

from pydantic import Field

from .link import Link
from .object import Object


class Collection(Object):
    type: Optional[str] = Field(default="Collection", kw_only=True)

    total_items: Optional[int] = Field(default=None, ge=0)
    current: Optional[str | dict | Link] = Field(default=None)
    first: Optional[str | dict | Link] = Field(default=None)
    last: Optional[str | dict | Link] = Field(default=None)
    items: Optional[List[Object | Link]] = Field(default=None)
    ordered_items: Optional[List[Object | Link]] = Field(default=None)


class CollectionPage(Collection):
    type: Optional[str] = Field(default="CollectionPage", kw_only=True)

    part_of: Optional[str | Collection | Link] = Field(default=None)

    next: Optional[str | CollectionPage | Link] = Field(default=None)
    prev: Optional[str | CollectionPage | Link] = Field(default=None)


class OrderedCollection(Collection):
    type: Optional[str] = Field(default="OrderedCollection", kw_only=True)


class OrderedCollectionPage(CollectionPage):
    type: Optional[str] = Field(default="OrderedCollectionPage", kw_only=True)

    start_index: Optional[int] = Field(default=None, ge=0)
