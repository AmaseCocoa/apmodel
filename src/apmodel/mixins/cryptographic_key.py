from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pydantic import BaseModel, PrivateAttr


class CryptographicKeyMixin(BaseModel):
    _public_key_cache: dict[str, Any] = PrivateAttr(default_factory=dict)

    @property
    def public_key(self) -> rsa.RSAPublicKey | None:
        if "public_key" in self._public_key_cache:
            return self._public_key_cache["public_key"]

        match self.public_key_pem:
            case str(s):
                k = s.encode("utf-8")
            case bytes(b):
                k = b
            case _:
                return None

        try:
            pub = serialization.load_pem_public_key(k)
        except (ValueError, TypeError):
            return None

        match pub:
            case rsa.RSAPublicKey():
                self._public_key_cache["public_key"] = pub
                return pub
            case _:
                raise ValueError(f"Unsupported Key Type: Expected RSAPublicKey, got {type(pub)}")

    @public_key.setter
    def public_key(self, k: rsa.RSAPublicKey | rsa.RSAPrivateKey) -> None:
        match k:
            case rsa.RSAPrivateKey():
                k = k.public_key()
            case rsa.RSAPublicKey():
                pass
            case _:
                raise TypeError("Must be RSA Public or Private Key")

        self._public_key_cache["public_key"] = k
        self.public_key_pem = k.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")
