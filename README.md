# apmodel

ActivityStreams 2.0 / ActivityPub model library for Python, built on [Pydantic v2](https://docs.pydantic.dev/).

- **Parse** ActivityPub JSON-LD payloads into typed Python objects with a single `load()` call.
- **Serialize** objects back to ActivityPub-compliant JSON with `obj.dump()`.
- **Includes** WebFinger helpers, NodeInfo support, and FEP-8b32 Multikey / Data Integrity Proof types.

## Installation

```bash
pip install apmodel
```

## Documentation

Full documentation lives in [`docs/`](docs/index.md).  
Migration guide from 0.5.x: [`docs/migration.md`](docs/migration.md).

## Links

- [apsig — HTTP Signature implementation for ActivityPub](https://github.com/AmaseCocoa/apsig)
- [apkit — ActivityPub toolkit](https://github.com/AmaseCocoa/apkit)
- [Official Fedi account](https://hollo.amase.cc/@apkit)