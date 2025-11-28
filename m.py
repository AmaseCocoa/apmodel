from __future__ import annotations

from pydantic import BaseModel, Field, conlist, constr
from typing import Optional, List, Union, Dict, Any
from datetime import date, datetime

class Object(BaseModel):
    """
    Auto-generated Pydantic model for Object.
    """
    
    id: Any = Field(
default=None,alias=None,    )
    
    type: Any = Field(
default=None,alias=None,    )
    
    subject: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    relationship: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    actor: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    attributedTo: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    attachment: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    bcc: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    bto: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    cc: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    context: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    current: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    first: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    generator: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    icon: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    image: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    inReplyTo: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    items: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    instrument: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    orderedItems: Union[str, 'Link', 'Object'] = Field(
default=None,alias="items",    )
    
    last: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    location: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    next: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    object: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    oneOf: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    anyOf: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    closed: datetime = Field(
default=None,alias=None,    )
    
    origin: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    accuracy: float = Field(
default=None,alias=None,    )
    
    prev: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    preview: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    replies: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    result: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    audience: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    partOf: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    tag: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    target: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    to: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    url: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    altitude: float = Field(
default=None,alias=None,    )
    
    content: Any = Field(
default=None,alias=None,    )
    
    contentMap: Any = Field(
default=None,alias="content",    )
    
    name: Any = Field(
default=None,alias=None,    )
    
    nameMap: Any = Field(
default=None,alias="name",    )
    
    duration: str = Field(
default=None,alias=None,    )
    
    endTime: datetime = Field(
default=None,alias=None,    )
    
    height: int = Field(
default=None,alias=None,    )
    
    href: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    hreflang: Any = Field(
default=None,alias=None,    )
    
    latitude: float = Field(
default=None,alias=None,    )
    
    longitude: float = Field(
default=None,alias=None,    )
    
    mediaType: Any = Field(
default=None,alias=None,    )
    
    published: datetime = Field(
default=None,alias=None,    )
    
    radius: float = Field(
default=None,alias=None,    )
    
    rel: Any = Field(
default=None,alias=None,    )
    
    startIndex: int = Field(
default=None,alias=None,    )
    
    startTime: datetime = Field(
default=None,alias=None,    )
    
    summary: Any = Field(
default=None,alias=None,    )
    
    summaryMap: Any = Field(
default=None,alias="summary",    )
    
    totalItems: int = Field(
default=None,alias=None,    )
    
    units: Any = Field(
default=None,alias=None,    )
    
    updated: datetime = Field(
default=None,alias=None,    )
    
    width: int = Field(
default=None,alias=None,    )
    
    describes: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    formerType: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    deleted: datetime = Field(
default=None,alias=None,    )
    
    inbox: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    outbox: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    following: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    followers: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    streams: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    preferredUsername: Any = Field(
default=None,alias=None,    )
    
    endpoints: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    uploadMedia: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    proxyUrl: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    liked: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    oauthAuthorizationEndpoint: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    oauthTokenEndpoint: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    provideClientKey: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    signClientKey: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    sharedInbox: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    source: Any = Field(
default=None,alias=None,    )
    
    likes: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    shares: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
    
    alsoKnownAs: Union[str, 'Link', 'Object'] = Field(
default=None,alias=None,    )
