# apmodel

ActivityStreams 2.0 / ActivityPub model library for Python, built on [Pydantic v2](https://docs.pydantic.dev/).

- **Parse** ActivityPub JSON-LD payloads into typed Python objects with a single `load()` call.
- **Serialize** objects back to ActivityPub-compliant JSON with `obj.dump()`.
- **Includes** WebFinger helpers, NodeInfo support, and FEP-8b32 Multikey / Data Integrity Proof types.

## Installation

```bash
pip install apmodel
```

## Quick start

```python
import json
import apmodel

# --- Parse an incoming payload ---
raw = {
    "@context": "https://www.w3.org/ns/activitystreams",
    "type": "Note",
    "id": "https://example.com/notes/1",
    "content": "Hello World",
    "attributedTo": "https://example.com/actors/alice",
}
note = apmodel.load(raw)
print(note.content)        # "Hello World"
print(note.attributed_to)  # "https://example.com/actors/alice"

# --- Serialise back to a dict (ready for json.dumps) ---
data = note.dump()
print(json.dumps(data, indent=2))
```

## Core concepts

### `load(data)` — parse a payload

`apmodel.load()` inspects the `type` field (and `@context` for extension types) and returns
the most specific model class it knows about, or `None` when the type is unrecognised.

```python
from apmodel import load

activity = load({
    "@context": "https://www.w3.org/ns/activitystreams",
    "type": "Create",
    "id": "https://example.com/activities/1",
    "actor": "https://example.com/actors/alice",
    "object": {
        "type": "Note",
        "id": "https://example.com/notes/1",
        "content": "Hello!",
    }
})

from apmodel.activity.create import Create
from apmodel.objects.note import Note

assert isinstance(activity, Create)
assert isinstance(activity.object, Note)
```

### `obj.dump()` — serialise to dict

`dump()` (an alias for `model_dump()`) returns a plain `dict` suitable for `json.dumps()`.
`@context` is automatically assembled from the object graph — you never have to set it by hand.

```python
from apmodel.objects.note import Note

note = Note(
    id="https://example.com/notes/1",
    content="Hello World",
    attributed_to="https://example.com/actors/alice",
    to=["https://www.w3.org/ns/activitystreams#Public"],
)
print(note.dump())
# {
#   "id": "https://example.com/notes/1",
#   "attributedTo": "https://example.com/actors/alice",
#   "content": "Hello World",
#   "to": ["https://www.w3.org/ns/activitystreams#Public"],
#   "type": "Note",
#   "@context": ["https://www.w3.org/ns/activitystreams"]
# }
```

Python field names use **snake_case**; they are automatically serialised to **camelCase** in the
output (e.g. `attributed_to` → `attributedTo`, `preferred_username` → `preferredUsername`).

### Field access

```python
actor = load(raw_actor_dict)

# Python snake_case attribute
print(actor.preferred_username)

# Extra / unknown fields are stored in model_extra
print(actor.model_extra.get("_misskey_summary"))
```

## Models

### Core types (`apmodel.core`)

| Class | Description |
|---|---|
| `Object` | Base ActivityStreams object |
| `Link` | ActivityStreams Link |
| `Activity` | Base activity |
| `IntransitiveActivity` | Activity without an object |
| `Collection` | Ordered/Unordered collection base |
| `OrderedCollection` | Ordered collection |
| `CollectionPage` | Page of a collection |
| `OrderedCollectionPage` | Page of an ordered collection |

### Actor types (`apmodel.objects`)

```python
from apmodel.objects import Person, Application, Group, Organization, Service, Actor
```

All actor types share these fields (in addition to the `Object` fields):

| Python field | JSON key | Type |
|---|---|---|
| `preferred_username` | `preferredUsername` | `str \| None` |
| `inbox` | `inbox` | `str \| OrderedCollection \| None` |
| `outbox` | `outbox` | `str \| OrderedCollection \| None` |
| `followers` | `followers` | `str \| Collection \| None` |
| `following` | `following` | `str \| Collection \| None` |
| `public_key` | `publicKey` | `CryptographicKey \| None` |
| `assertion_method` | `assertionMethod` | `list[Multikey]` |
| `discoverable` | `discoverable` | `bool \| None` |
| `indexable` | `indexable` | `bool \| None` |
| `endpoints` | `endpoints` | `ActorEndpoints \| None` |

#### Key helpers

```python
from apmodel import load

actor = load(raw_actor)

# actor.keys — combined list of CryptographicKey + Multikey objects
for key in actor.keys:
    print(key.id)

# actor.get_key(key_id) — look up by ID
key = actor.get_key("https://example.com/actors/alice#main-key")
```

### Object vocabulary (`apmodel.objects`)

```python
from apmodel.objects import (
    Note, Article, Document, Image, Audio, Video, Page,
    Event, Place, Profile, Tombstone, Mention, Hashtag, Relationship,
)
```

### Activity vocabulary (`apmodel.activity`)

```python
from apmodel.activity import (
    Accept, TentativeAccept,
    Add, Announce, Arrive,
    Block, Create, Delete, Dislike, Flag, Follow,
    Ignore, Invite, Join, Leave, Like, Listen,
    Move, Offer, Question, Read, Reject, TentativeReject,
    Remove, Travel, Undo, Update, View,
)
```

## Cryptographic key types

### `CryptographicKey` — RSA public key (HTTP Signatures / Mastodon-style)

```python
from apmodel.security import CryptographicKey

key = CryptographicKey(
    id="https://example.com/actors/alice#main-key",
    owner="https://example.com/actors/alice",
    public_key_pem="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n",
)

# .public_key property returns a cryptography RSAPublicKey object
rsa_key = key.public_key
```

### `Multikey` — FEP-8b32 / W3C CID multibase key (Ed25519 or RSA)

```python
from apmodel.cid import Multikey

# Construct with a raw key object — encoding is automatic
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

priv = Ed25519PrivateKey.generate()
mk = Multikey(
    id="https://example.com/actors/alice#ed25519-key",
    controller="https://example.com/actors/alice",
    public_key_multibase=priv.public_key(),  # accepts key objects directly
)

# .public_key / .private_key — decoded cryptography key objects
pub = mk.public_key
```

### `DataIntegrityProof`

```python
from apmodel.cid import DataIntegrityProof
```

## Context management

`Context` parses and deduplicates JSON-LD `@context` values.

```python
from apmodel.context import Context

ctx = Context.parse([
    "https://www.w3.org/ns/activitystreams",
    {"schema": "https://schema.org/"},
])

# Attach to a model
from apmodel.objects.note import Note

note = Note(
    id="https://example.com/notes/1",
    content="Hello",
    ctx=ctx,
)
# The extra context items are merged into @context on dump()
```

## NodeInfo

```python
from apmodel.nodeinfo import Nodeinfo, from_dict

# Parse a NodeInfo document
nodeinfo = from_dict(raw_nodeinfo_dict)
print(nodeinfo.software.name)
print(nodeinfo.version)           # "2.0" or "2.1"
print(nodeinfo.open_registrations)
```

### `NodeinfoFactory`

```python
from apmodel.nodeinfo.factory import NodeinfoFactory

# Build a NodeInfo 2.1 document
from apmodel.nodeinfo import Nodeinfo, Software, Usage, Users

nodeinfo = Nodeinfo(
    version="2.1",
    software=Software(name="myapp", version="1.0.0"),
    protocols=["activitypub"],
    open_registrations=False,
    usage=Usage(users=Users(total=42)),
)
data = nodeinfo.model_dump(by_alias=True)
```

## WebFinger

```python
from apmodel.webfinger import Resource, Result

# Parse an acct: URI
resource = Resource.parse("alice@example.com")
print(resource.username)   # "alice"
print(resource.host)       # "example.com"
print(str(resource))       # "acct:alice@example.com"

# Parse a WebFinger JRD response
result = Result.from_dict(jrd_dict)
print(result.subject)
for link in result.links:
    print(link.rel, link.href)

# Serialise back to JRD
jrd = result.to_json()
```

## Enums

```python
from apmodel.enums import Visibility

Visibility.PUBLIC   # "https://www.w3.org/ns/activitystreams#Public"
```

## Extension types

### Mastodon / Pleroma

```python
from apmodel.mastodon import Emoji
```

### LitePub

```python
from apmodel.litepub import EmojiReact
```

### schema.org

```python
from apmodel.schema import PropertyValue
```

## Extending the type registry

If you have custom ActivityPub types, register them with the `TypeInferencer`:

```python
from apmodel.base import AS2Model
from apmodel.inference import TypeInferencer

class MyCustomType(AS2Model):
    type: str = "MyCustomType"
    my_field: str | None = None

from apmodel.loader import type_loader

type_loader.set("MyCustomType", MyCustomType)

# Now load() will resolve "type": "MyCustomType" → MyCustomType
```

## Links

- [apsig — HTTP Signature implementation for ActivityPub](https://github.com/AmaseCocoa/apsig)
- [apkit — ActivityPub toolkit](https://github.com/AmaseCocoa/apkit)
- [Official Fedi account](https://hollo.amase.cc/@apkit)