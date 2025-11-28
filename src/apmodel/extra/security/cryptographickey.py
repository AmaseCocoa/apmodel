from typing import Any, Optional, Union

from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pydantic import Field, field_serializer, field_validator

from ...types import ActivityPubModel


class CryptographicKey(ActivityPubModel):
    type: Optional[str] = Field(default="CryptographicKey", kw_only=True, frozen=True)

    id: Optional[str] = Field(default=None)
    owner: Optional[str] = Field(default=None)
    publicKeyPem: Optional[Union[rsa.RSAPublicKey, str, bytes]] = Field(
        default=None
    )

    _extra: dict = Field(default_factory=dict)

    @field_validator("publicKeyPem", mode="before")
    @classmethod
    def validate_public_key_pem(cls, v: Any) -> rsa.RSAPublicKey:
        if v is None:
            raise ValueError("publicKeyPem cannot be None.")

        if isinstance(v, rsa.RSAPublicKey):
            return v

        if isinstance(v, str):
            pem_data = v.encode("utf-8")
        elif isinstance(v, bytes):
            pem_data = v
        else:
            raise ValueError(
                f"Unsupported input type for publicKeyPem: {type(v)}"
            )

        try:
            pub_key = serialization.load_pem_public_key(pem_data)

            if isinstance(pub_key, rsa.RSAPublicKey):
                return pub_key
            else:
                raise ValueError(
                    f"Unsupported Key Type: Expected RSAPublicKey, got {type(pub_key)}"
                )

        except (ValueError, UnsupportedAlgorithm, TypeError) as e:
            raise ValueError(f"Invalid PEM public key format or value: {e}")

    @field_serializer("publicKeyPem", when_used="always")
    def serialize_key_to_pem(self, value: rsa.RSAPublicKey, info) -> str:
        if not isinstance(value, rsa.RSAPublicKey):
            raise TypeError("Expected RSAPublicKey for serialization.")

        pem_string = value.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

        return pem_string
