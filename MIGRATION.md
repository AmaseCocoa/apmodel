# Migration guide: 0.5.x → 0.6.x

0.6.x is a ground-up rewrite of apmodel.  
The public API has changed significantly.  
This document lists every breaking change and shows how to update your code.

---

## Table of contents

1. [Base class](#1-base-class)
2. [Serialisation](#2-serialisation)
3. [Parsing (`load`)](#3-parsing-load)
4. [Import paths](#4-import-paths)
5. [Context](#5-context)
6. [Field names](#6-field-names)
7. [Extra fields](#7-extra-fields)
8. [Cryptographic keys](#8-cryptographic-keys)
9. [NodeInfo](#9-nodeinfo)
10. [Removed APIs](#10-removed-apis)
11. [New features in 0.6.x](#11-new-features-in-06x)

---

## 1. Base class

The base class was replaced.

| | 0.5.x | 0.6.x |
|---|---|---|
| Class name | `ActivityPubModel` | `AS2Model` |
| Module | `apmodel.types` | `apmodel.base` |
| Backed by | `dataclasses.dataclass` | Pydantic v2 `BaseModel` |

**Before:**

```python
from apmodel.types import ActivityPubModel

class MyModel(ActivityPubModel):
    ...
```

**After:**

```python
from apmodel.base import AS2Model

class MyModel(AS2Model):
    type: str = "MyModel"
    my_field: str | None = None
```

> Custom models must be registered with `type_loader.set()` so that `load()` resolves them.
> See [Extending the type registry](README.md#extending-the-type-registry).

---

## 2. Serialisation

### `dump()` / `to_json()` — standalone function removed

In 0.5.x there was a standalone `dump(model)` function that returned a JSON **string**.  
In 0.6.x serialisation is a **method** on every model and returns a **dict**.

**Before:**

```python
from apmodel import dump

json_str = dump(note)
```

**After:**

```python
import json

# dict
data = note.dump()

# JSON string
json_str = json.dumps(note.dump())
```

`dump()` is a thin alias for the standard Pydantic `model_dump()`.  
Both methods are available:

```python
note.dump()                     # equivalent
note.model_dump()               # equivalent
```

### `to_json()` removed

`ActivityPubModel.to_json()` no longer exists. Use `model.dump()`.

---

## 3. Parsing (`load`)

The return type changed.

| | 0.5.x | 0.6.x |
|---|---|---|
| Return type | `ActivityPubModel \| dict` | `AS2Model \| None` |

**Before:**

```python
from apmodel import load

result = load(data)
if isinstance(result, dict):
    # unrecognised type — raw dict returned
    ...
```

**After:**

```python
from apmodel import load

result = load(data)
if result is None:
    # unrecognised type
    ...
```

---

## 4. Import paths

Many modules were reorganised.

### Actor types

| 0.5.x | 0.6.x |
|---|---|
| `from apmodel.vocab import Person` | `from apmodel.objects import Person` |
| `from apmodel.vocab import Person, Application, Group, Organization, Service` | `from apmodel.objects import Person, Application, Group, Organization, Service` |
| `from apmodel.vocab.actor import Person` | `from apmodel.objects.actor import Person` |

### Object vocabulary

| 0.5.x | 0.6.x |
|---|---|
| `from apmodel.vocab import Note` | `from apmodel.objects import Note` |
| `from apmodel.vocab import Article, Document, …` | `from apmodel.objects import Article, Document, …` |
| `from apmodel.vocab.object.note import Note` | `from apmodel.objects.note import Note` |

### Activity vocabulary

| 0.5.x | 0.6.x |
|---|---|
| `from apmodel.vocab.activity import Create` | `from apmodel.activity import Create` |
| `from apmodel.vocab.activity import Follow, Like, …` | `from apmodel.activity import Follow, Like, …` |

### Security / CID

| 0.5.x | 0.6.x |
|---|---|
| `from apmodel.extra.security import CryptographicKey` | `from apmodel.security import CryptographicKey` |
| `from apmodel.extra.cid import DataIntegrityProof, Multikey` | `from apmodel.cid import DataIntegrityProof, Multikey` |

### schema.org

| 0.5.x | 0.6.x |
|---|---|
| `from apmodel.extra.schema import PropertyValue` | `from apmodel.schema import PropertyValue` |

### Mastodon / LitePub extensions

| 0.5.x | 0.6.x |
|---|---|
| `from apmodel.extra import Emoji, Hashtag` | `from apmodel.mastodon import Emoji` |
| | `from apmodel.objects import Hashtag` |
| `from apmodel.extra import EmojiReact` | `from apmodel.litepub import EmojiReact` |

### Top-level convenience imports

All of the commonly used types are still available directly from `apmodel`:

```python
from apmodel import (
    load, to_dict,
    Object, Link, Activity, IntransitiveActivity,
    Collection, OrderedCollection, CollectionPage, OrderedCollectionPage,
    CryptographicKey, DataIntegrityProof, Multikey,
    Context, Visibility,
    Emoji, EmojiReact, PropertyValue,
    AS2Model, TypeInferencer,
)
```

---

## 5. Context

The context class was renamed and its API changed.

| | 0.5.x | 0.6.x |
|---|---|---|
| Class name | `LDContext` | `Context` |
| Module | `apmodel.context` | `apmodel.context` |
| Construction | `LDContext(value)` constructor | `Context.parse(value)` class method |
| Attach to model | `_context=LDContext(value)` | `ctx=Context.parse(value)` |

**Before:**

```python
from apmodel.context import LDContext

ctx = LDContext(["https://www.w3.org/ns/activitystreams", "https://example.org/ns"])
obj = Note(_context=ctx, ...)
```

**After:**

```python
from apmodel.context import Context

ctx = Context.parse([
    "https://www.w3.org/ns/activitystreams",
    "https://example.org/ns",
])
obj = Note(ctx=ctx, ...)
```

The `value` property returns the full merged context list:

```python
ctx.value   # list of str / dict items
```

---

## 6. Field names

All Python field names are now **snake_case**.  
Pydantic's alias generator maps them to **camelCase** for JSON automatically.

| Python (0.6.x) | JSON |
|---|---|
| `preferred_username` | `preferredUsername` |
| `attributed_to` | `attributedTo` |
| `public_key` | `publicKey` |
| `public_key_pem` | `publicKeyPem` |
| `public_key_multibase` | `publicKeyMultibase` |
| `in_reply_to` | `inReplyTo` |
| `open_registrations` | `openRegistrations` |
| `total_items` | `totalItems` |

You can always pass **either** form when constructing a model thanks to
`populate_by_name=True`:

```python
# Both are accepted
Note(attributed_to="https://example.com/actor")
Note(attributedTo="https://example.com/actor")
```

In 0.5.x, some fields used camelCase directly in the dataclass definition.
In 0.6.x only the snake_case form is the Python attribute.

---

## 7. Extra fields

Unknown / extension fields are stored differently.

| | 0.5.x | 0.6.x |
|---|---|---|
| Storage | `model._extra` (private dict) | `model.model_extra` (standard Pydantic dict) |

**Before:**

```python
value = actor._extra.get("_misskey_summary")
```

**After:**

```python
value = actor.model_extra.get("_misskey_summary")
```

---

## 8. Cryptographic keys

### `CryptographicKey`

The module path changed (see [Import paths](#4-import-paths)).  
The `.public_key` property still returns a `cryptography` `RSAPublicKey` object.

```python
from apmodel.security import CryptographicKey   # new path

key = CryptographicKey(
    id="https://example.com/actors/alice#main-key",
    owner="https://example.com/actors/alice",
    public_key_pem="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n",
)
rsa_pub = key.public_key   # cryptography.hazmat RSAPublicKey
```

### `Multikey` (FEP-8b32)

The module path changed (see [Import paths](#4-import-paths)).

```python
from apmodel.cid import Multikey   # new path
```

---

## 9. NodeInfo

The `NodeinfoFactory` class was removed from `apmodel.nodeinfo`.  
Use `apmodel.nodeinfo.factory.NodeinfoFactory` directly, or build a `Nodeinfo` model
manually and call `model_dump(by_alias=True)`.

```python
# 0.6.x
from apmodel.nodeinfo import Nodeinfo, Software, Usage, Users
from apmodel.nodeinfo.factory import NodeinfoFactory

nodeinfo = Nodeinfo(
    version="2.1",
    software=Software(name="myapp", version="1.0.0"),
    protocols=["activitypub"],
    open_registrations=False,
)
data = nodeinfo.model_dump(by_alias=True)
```

---

## 10. Removed APIs

| Removed in 0.6.x | Replacement |
|---|---|
| `from apmodel import dump` (function) | `model.dump()` method |
| `model.to_json()` | `model.dump()` |
| `ActivityPubModel` | `AS2Model` |
| `LDContext` | `Context` |
| `model._extra` | `model.model_extra` |
| `from apmodel.vocab import …` | `from apmodel.objects import …` |
| `from apmodel.vocab.activity import …` | `from apmodel.activity import …` |
| `from apmodel.extra.security import …` | `from apmodel.security import …` |
| `from apmodel.extra.cid import …` | `from apmodel.cid import …` |
| `from apmodel.extra.schema import …` | `from apmodel.schema import …` |
| `from apmodel.extra import Emoji, Hashtag` | `from apmodel.mastodon import Emoji` / `from apmodel.objects import Hashtag` |

---

## 11. New features in 0.6.x

- **Pydantic v2 integration** — all models are proper Pydantic `BaseModel` subclasses
  with full validation, serialisation, and JSON schema support.
- **WebFinger helpers** — `apmodel.webfinger` provides `Resource`, `Link`, and `Result`
  dataclasses for parsing and building WebFinger JRD responses.
- **Automatic `@context` assembly** — `dump()` collects context URLs from the entire
  object graph and merges them into a single top-level `@context` array.
- **`actor.keys` / `actor.get_key()`** — convenience helpers that unify
  `publicKey` (RSA) and `assertionMethod` (Multikey) into one list.
- **`TypeInferencer.set()`** — register custom types at runtime without subclassing.
- **`Visibility` enum** — `apmodel.enums.Visibility` for the AS2 Public audience URI.
- **`to_dict()` helper** — `apmodel.to_dict(model)` as a functional alias for
  `model.dump()`.
