from __future__ import annotations
from typing import Optional, List, Union, Dict, Any
from datetime import date, datetime
from pydantic import BaseModel, Field

from .link import Link

class Object(BaseModel):
    """
    Model: Object
    """
    
    id: Optional[Any] = Field(
default=None,alias=None,    )
    
    type: Optional[Any] = Field(
default=None,alias=None,    )
    
    subject: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    relationship: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    attributedTo: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    attachment: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    bcc: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    bto: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    cc: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    context: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    current: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    first: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    generator: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    icon: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    image: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    inReplyTo: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    items: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    instrument: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    orderedItems: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias="items",    )
    
    last: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    location: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    next: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    object: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    oneOf: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    anyOf: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    closed: Optional[datetime] = Field(
default=None,alias=None,    )
    
    origin: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    accuracy: Optional[float] = Field(
default=None,alias=None,    )
    
    prev: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    preview: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    replies: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    result: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    audience: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    partOf: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    tag: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    target: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    to: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    url: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    altitude: Optional[float] = Field(
default=None,alias=None,    )
    
    content: Optional[Any] = Field(
default=None,alias=None,    )
    
    contentMap: Optional[Any] = Field(
default=None,alias="content",    )
    
    name: Optional[Any] = Field(
default=None,alias=None,    )
    
    nameMap: Optional[Any] = Field(
default=None,alias="name",    )
    
    duration: Optional[str] = Field(
default=None,alias=None,    )
    
    endTime: Optional[datetime] = Field(
default=None,alias=None,    )
    
    height: Optional[int] = Field(
default=None,alias=None,    )
    
    href: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    hreflang: Optional[Any] = Field(
default=None,alias=None,    )
    
    latitude: Optional[float] = Field(
default=None,alias=None,    )
    
    longitude: Optional[float] = Field(
default=None,alias=None,    )
    
    mediaType: Optional[Any] = Field(
default=None,alias=None,    )
    
    published: Optional[datetime] = Field(
default=None,alias=None,    )
    
    radius: Optional[float] = Field(
default=None,alias=None,    )
    
    rel: Optional[Any] = Field(
default=None,alias=None,    )
    
    startIndex: Optional[int] = Field(
default=None,alias=None,    )
    
    startTime: Optional[datetime] = Field(
default=None,alias=None,    )
    
    summary: Optional[Any] = Field(
default=None,alias=None,    )
    
    summaryMap: Optional[Any] = Field(
default=None,alias="summary",    )
    
    totalItems: Optional[int] = Field(
default=None,alias=None,    )
    
    units: Optional[Any] = Field(
default=None,alias=None,    )
    
    updated: Optional[datetime] = Field(
default=None,alias=None,    )
    
    width: Optional[int] = Field(
default=None,alias=None,    )
    
    describes: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    formerType: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    deleted: Optional[datetime] = Field(
default=None,alias=None,    )
    
    inbox: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    outbox: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    following: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    followers: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    streams: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    preferredUsername: Optional[Any] = Field(
default=None,alias=None,    )
    
    endpoints: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    uploadMedia: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    proxyUrl: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    liked: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    oauthAuthorizationEndpoint: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    oauthTokenEndpoint: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    provideClientKey: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    signClientKey: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    sharedInbox: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    source: Optional[Any] = Field(
default=None,alias=None,    )
    
    likes: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    shares: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    alsoKnownAs: Optional[Union[str, 'Link', 'Object']] = Field(
default=None,alias=None,    )
    
    test: Optional[str] = Field(
default=None,alias=None,    )