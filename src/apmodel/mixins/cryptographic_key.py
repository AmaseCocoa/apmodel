from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


class CryptographicKeyMixin:
    def __init__(self, **data):
        super().__init__(**data)
        # Initialize cache for storing computed public key
        if not hasattr(self, '__public_key_cache'):
            object.__setattr__(self, '__public_key_cache', {})

    @property
    def public_key(self) -> rsa.RSAPublicKey | None:
        cache = object.__getattribute__(self, '__public_key_cache')
        if 'public_key' in cache:
            return cache['public_key']

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
                cache['public_key'] = pub
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

        cache = object.__getattribute__(self, '__public_key_cache')
        cache['public_key'] = k
        self.public_key_pem = k.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")
