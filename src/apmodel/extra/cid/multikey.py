from typing import Any, Optional, Union

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, rsa
from multiformats import multibase, multicodec
from pydantic import Field, field_serializer, field_validator

from ...types import ActivityPubModel

PublicKeyTypes = Union[str, ed25519.Ed25519PublicKey, rsa.RSAPublicKey]
PrivateKeyTypes = Union[str, ed25519.Ed25519PrivateKey, rsa.RSAPrivateKey]


class Multikey(ActivityPubModel):
    type: Optional[str] = Field(default="Multikey", kw_only=True)

    id: str
    controller: str
    publicKeyMultibase: Optional[PublicKeyTypes] = Field(default=None)
    secretKeyMultibase: Optional[PrivateKeyTypes] = Field(default=None)

    _extra: dict = Field(default_factory=dict)

    @field_validator("publicKeyMultibase", mode="before")
    @classmethod
    def validate_public_key(cls, v: Any) -> PublicKeyTypes:
        if not isinstance(v, str):
            return v

        try:
            decoded = multibase.decode(v)
            codec, data = multicodec.unwrap(decoded)

            if codec.name == "ed25519-pub":
                pub_key = ed25519.Ed25519PublicKey.from_public_bytes(data)
                return pub_key

            elif codec.name == "rsa-pub":
                pub_key = serialization.load_der_public_key(data)
                if not isinstance(pub_key, rsa.RSAPublicKey):
                    raise ValueError(
                        f"Unsupported Key Type for rsa-pub: {type(pub_key)}"
                    )
                return pub_key

            else:
                raise ValueError(f"Unsupported Codec: {codec.name}")

        except Exception as e:
            raise ValueError(f"Invalid public key format or value: {e}")

    @field_validator("secretKeyMultibase", mode="before")
    @classmethod
    def validate_private_key(cls, v: Any) -> PrivateKeyTypes:
        if v is None or not isinstance(v, str):
            return v

        try:
            decoded = multibase.decode(v)
            codec, data = multicodec.unwrap(decoded)

            if codec.name == "ed25519-priv":
                priv_key = ed25519.Ed25519PrivateKey.from_private_bytes(data)
                return priv_key

            elif codec.name == "rsa-priv":
                priv_key = serialization.load_der_private_key(
                    data, password=None
                )
                if not isinstance(priv_key, rsa.RSAPrivateKey):
                    raise ValueError(
                        f"Unsupported Key Type for rsa-priv: {type(priv_key)}"
                    )
                return priv_key

            else:
                raise ValueError(f"Unsupported Codec: {codec.name}")

        except Exception as e:
            raise ValueError(f"Invalid private key format or value: {e}")

    @field_serializer(
        "publicKeyMultibase", "secretKeyMultibase", when_used="always"
    )
    def serialize_key_to_multibase(self, value: Any, info) -> str:
        if isinstance(value, str):
            return value

        if isinstance(value, rsa.RSAPrivateKey):
            wrapped = multicodec.wrap(
                "rsa-priv",
                value.private_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                ),
            )
            return multibase.encode(wrapped, "base58btc")

        elif isinstance(value, ed25519.Ed25519PrivateKey):
            wrapped = multicodec.wrap(
                "ed25519-priv",
                value.private_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PrivateFormat.Raw,
                    encryption_algorithm=serialization.NoEncryption(),
                ),
            )
            return multibase.encode(wrapped, "base58btc")

        elif isinstance(value, rsa.RSAPublicKey):
            wrapped = multicodec.wrap(
                "rsa-pub",
                value.public_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PublicFormat.PKCS1,
                ),
            )
            return multibase.encode(wrapped, "base58btc")

        elif isinstance(value, ed25519.Ed25519PublicKey):
            wrapped = multicodec.wrap(
                "ed25519-pub",
                value.public_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PublicFormat.Raw,
                ),
            )
            return multibase.encode(wrapped, "base58btc")

        return value
