# About
This Repository is source code of apmodel.

apmodel is model implementions of Activity Streams 2.0, CryptographicKey (Security Vocabulary v1), Multikey and DataIntegrityProof (Controlled Identifiers v1.0), PropertyValue (schema.org).

## features
- load function that automatically reads the type key from json and converts it to the correct model, returns json if there is no matching model
- If there is no key corresponding to the model, add it to the model's dictionary `_extra`.