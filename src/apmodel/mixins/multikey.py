from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, rsa
from multiformats import multibase, multicodec
from pydantic import PrivateAttr, field_validator


class MultikeyMixin:
    _public_key: ed25519.Ed25519PublicKey | rsa.RSAPublicKey | None = PrivateAttr(None)
    _private_key: ed25519.Ed25519PrivateKey | rsa.RSAPrivateKey | None = PrivateAttr(None)
    

    @field_validator(
        "public_key_multibase", "private_key_multibase", mode="before"
    )
    @classmethod
    def _convert_keys(
        cls,
        v: str
        | rsa.RSAPublicKey
        | ed25519.Ed25519PublicKey
        | rsa.RSAPrivateKey
        | ed25519.Ed25519PrivateKey
        | None,
    ) -> str | None:
        if isinstance(
            v,
            (
                rsa.RSAPublicKey,
                ed25519.Ed25519PublicKey,
                rsa.RSAPrivateKey,
                ed25519.Ed25519PrivateKey,
            ),
        ):
            return cls.__mb_encode(v)
        return v

    @staticmethod
    def __mb_encode(
        k: ed25519.Ed25519PublicKey
        | rsa.RSAPublicKey
        | ed25519.Ed25519PrivateKey
        | rsa.RSAPrivateKey,
    ) -> str:
        if isinstance(k, rsa.RSAPublicKey):
            codec, data = (
                "rsa-pub",
                k.public_bytes(
                    serialization.Encoding.DER, serialization.PublicFormat.PKCS1
                ),
            )
        elif isinstance(k, ed25519.Ed25519PublicKey):
            codec, data = (
                "ed25519-pub",
                k.public_bytes(
                    serialization.Encoding.Raw, serialization.PublicFormat.Raw
                ),
            )
        elif isinstance(k, rsa.RSAPrivateKey):
            codec, data = (
                "rsa-priv",
                k.private_bytes(
                    serialization.Encoding.DER,
                    serialization.PrivateFormat.PKCS8,
                    serialization.NoEncryption(),
                ),
            )
        elif isinstance(k, ed25519.Ed25519PrivateKey):
            codec, data = (
                "ed25519-priv",
                k.private_bytes(
                    serialization.Encoding.Raw,
                    serialization.PrivateFormat.Raw,
                    serialization.NoEncryption(),
                ),
            )
        else:
            raise ValueError(f"Unsupported key type: {type(k)}")

        wrapped = multicodec.wrap(codec, data)
        return multibase.encode(wrapped, "base58btc")

    @staticmethod
    def __mb_decode(
        v: str,
    ) -> (
        ed25519.Ed25519PublicKey
        | rsa.RSAPublicKey
        | ed25519.Ed25519PrivateKey
        | rsa.RSAPrivateKey
    ):
        decoded = multibase.decode(v)
        codec, data = multicodec.unwrap(decoded)

        match codec.name:
            case "ed25519-pub":
                k = ed25519.Ed25519PublicKey.from_public_bytes(data)
            case "rsa-pub":
                k = serialization.load_der_public_key(data)
            case "ed25519-priv":
                k = ed25519.Ed25519PrivateKey.from_private_bytes(data)
            case "rsa-priv":
                k = serialization.load_der_private_key(data, password=None)
            case _:
                raise ValueError(f"Unsupported Codec: {codec.name}")

        match k:
            case (
                rsa.RSAPrivateKey()
                | ed25519.Ed25519PrivateKey()
                | rsa.RSAPublicKey()
                | ed25519.Ed25519PublicKey()
            ):
                return k
            case _:
                raise ValueError(
                    f"Unsupported Key Type for {codec.name}: {type(k)}"
                )

    @property
    def private_key(
        self,
    ) -> ed25519.Ed25519PrivateKey | rsa.RSAPrivateKey | None:
        if (priv := self._private_key) is not None:
            return priv

        match self.private_key_multibase:
            case str(s):
                priv = self.__mb_decode(s)
            case _:
                return None

        match priv:
            case rsa.RSAPrivateKey() | ed25519.Ed25519PrivateKey():
                self._private_key = priv
                return priv
            case _:
                raise ValueError(
                    f"Unsupported Key Type; Expected RSAPrivateKey or Ed25519PrivateKey, got {type(priv)}"
                )

    @private_key.setter
    def private_key(
        self,
        k: rsa.RSAPrivateKey | ed25519.Ed25519PrivateKey,
    ) -> None:
        match k:
            case rsa.RSAPrivateKey() | ed25519.Ed25519PrivateKey():
                pass
            case _:
                raise TypeError("Must be RSAPrivateKey or Ed25519PrivateKey")

        self._private_key = k
        self.private_key_multibase = self.__mb_encode(k)

    @property
    def public_key(self) -> ed25519.Ed25519PublicKey | rsa.RSAPublicKey | None:
        if (pub := self._public_key) is not None:
            return pub

        match self.public_key_multibase:
            case str(s):
                pub = self.__mb_decode(s)
            case _:
                return None

        match pub:
            case rsa.RSAPublicKey() | ed25519.Ed25519PublicKey():
                self._public_key = pub
                return pub
            case _:
                raise ValueError(
                    f"Unsupported Key Type; Expected RSAPublicKey or Ed25519PublcKey, got {type(pub)}"
                )

    @public_key.setter
    def public_key(
        self,
        k: rsa.RSAPublicKey
        | rsa.RSAPrivateKey
        | ed25519.Ed25519PrivateKey
        | ed25519.Ed25519PublicKey,
    ) -> None:
        match k:
            case rsa.RSAPrivateKey() | ed25519.Ed25519PrivateKey():
                k = k.public_key()
            case rsa.RSAPublicKey() | ed25519.Ed25519PublicKey():
                pass
            case _:
                raise TypeError("Must be RSA/Ed25519 Public or Private Key")

        self._public_key = k
        self.public_key_multibase = self.__mb_encode(k)
