from dataclasses import dataclass, field
from typing import Union

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from ...dumper import _serialize_model_to_json
from ...types import Undefined, ActivityPubModel

@dataclass
class CryptographicKey(ActivityPubModel):
    type: Union[str, Undefined] = field(default="CryptographicKey", kw_only=True)

    id: Union[str, Undefined] = field(default_factory=Undefined)
    owner: Union[str, Undefined] = field(default_factory=Undefined)
    publicKeyPem: Union[rsa.RSAPublicKey, str, bytes, Undefined] = field(default_factory=Undefined)

    _extra: dict = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.publicKeyPem, Undefined) and not isinstance(self.publicKeyPem, rsa.RSAPublicKey):
            pub_key = serialization.load_pem_public_key(self.publicKeyPem.encode("utf-8") if isinstance(self.publicKeyPem, str) else self.publicKeyPem)
            if isinstance(pub_key, rsa.RSAPublicKey):
                self.publicKeyPem = pub_key
            else:
                raise ValueError("Unsupported Key: {}".format(type(pub_key)))

    def to_json(self):
        if isinstance(self.publicKeyPem, rsa.RSAPublicKey):
            self.publicKeyPem = self.publicKeyPem.public_bytes(
                encoding=serialization.Encoding.PEM, 
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode("utf-8")
        data = _serialize_model_to_json(self)
        return data
