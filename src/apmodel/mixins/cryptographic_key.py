from typing import Protocol

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pydantic import PrivateAttr


class CryptographicKeyProtocol(Protocol):
    public_key_pem: bytes | str | None


class CryptographicKeyMixin(CryptographicKeyProtocol):
    _public_key: rsa.RSAPublicKey | None = PrivateAttr(None)

    @property
    def public_key(self) -> rsa.RSAPublicKey | None:
        if (pub := self._public_key) is not None:
            return pub

        match self.public_key_pem:
            case str(s):
                k = s.encode("utf-8")
            case bytes(b):
                k = b
            case _:
                return None

        pub = serialization.load_pem_public_key(k)

        match pub:
            case rsa.RSAPublicKey():
                self._public_key = pub
                return pub
            case _:
                raise ValueError(
                    f"Unsupported Key Type: Expected RSAPublicKey, got {type(pub)}"
                )

    @public_key.setter
    def public_key(self, k: rsa.RSAPublicKey | rsa.RSAPrivateKey) -> None:
        match k:
            case rsa.RSAPrivateKey():
                k = k.public_key()
            case rsa.RSAPublicKey():
                pass
            case _:
                raise TypeError("Must be RSA Public or Private Key")

        self._public_key = k
        self.public_key_pem = k.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")
