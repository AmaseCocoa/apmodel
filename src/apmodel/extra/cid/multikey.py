from dataclasses import field, asdict, dataclass
from typing import Union

from cryptography.hazmat.primitives.asymmetric import ed25519, rsa
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidKey
from multiformats import multicodec, multibase

from ...types import ActivityPubModel, Undefined

@dataclass
class Multikey(ActivityPubModel):
    type: Union[str, Undefined] = field(default="Multikey", kw_only=True)

    id: str
    controller: str
    publicKeyMultibase: Union[ed25519.Ed25519PublicKey | rsa.RSAPublicKey, str, Undefined] = field(default_factory=Undefined)
    secretKeyMultibase: Union[ed25519.Ed25519PrivateKey | rsa.RSAPrivateKey, str, Undefined] = field(default_factory=Undefined)
    
    _extra: dict = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.publicKeyMultibase, str):
            decoded = multibase.decode(self.publicKeyMultibase)
            codec, data = multicodec.unwrap(decoded)
            if codec.name == "ed25519-pub":
                try:
                    pub_key = ed25519.Ed25519PublicKey.from_public_bytes(data)
                    if isinstance(pub_key, ed25519.Ed25519PublicKey):
                        self.publicKeyMultibase = pub_key
                    else:
                        raise ValueError("Unsupported Key: {}".format(type(pub_key)))
                except InvalidKey:
                    raise Exception("Invalid ed25519 public key passed.")
            elif codec.name == "rsa-pub":
                try:
                    pub_key = serialization.load_der_public_key(data)
                    if isinstance(pub_key, rsa.RSAPublicKey):
                        self.publicKeyMultibase = pub_key
                    else:
                        raise ValueError("Unsupported Key: {}".format(type(pub_key)))
                except ValueError:
                    raise Exception("Invalid rsa public key passed.")
            else:
                raise ValueError("Unsupported Codec: {}".format(codec.name))
        elif isinstance(self.secretKeyMultibase, str):
            decoded = multibase.decode(self.secretKeyMultibase)
            codec, data = multicodec.unwrap(decoded)
            if codec.name == "ed25519-priv":
                try:
                    priv_key = ed25519.Ed25519PrivateKey.from_private_bytes(data)
                    if isinstance(priv_key, ed25519.Ed25519PrivateKey):
                        self.secretKeyMultibase = priv_key
                    else:
                        raise ValueError("Unsupported Key: {}".format(type(priv_key)))
                except InvalidKey:
                    raise Exception("Invalid ed25519 public key passed.")
            elif codec.name == "rsa-priv":
                try:
                    priv_key = serialization.load_der_private_key(data, password=None) # type: ignore
                    if isinstance(priv_key, rsa.RSAPrivateKey):
                        self.secretKeyMultibase = priv_key
                    else:
                        raise ValueError("Unsupported Key: {}".format(type(priv_key)))
                except ValueError:
                    raise Exception("Invalid rsa public key passed.")
            else:
                raise ValueError("Unsupported Codec: {}".format(codec.name))

    def to_json(self):
        data = asdict(self)
        extra = data.pop("_extra", {})
        data["@context"] = data.pop("_context")
        for key, value in list(data.items()):
            if isinstance(value, Undefined):
                del data[key]
            elif isinstance(value, ActivityPubModel):
                data[key] = value.to_json()
            elif isinstance(value, list):
                data[key] = [v.to_json() if isinstance(v, ActivityPubModel) else v for v in value]
            elif isinstance(value, rsa.RSAPrivateKey):
                wrapped = multicodec.wrap("rsa-priv", value.private_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PrivateFormat.Raw,
                    encryption_algorithm=serialization.NoEncryption()
                ))
                data[key] = multibase.encode(wrapped, "base58btc")
            elif isinstance(value, ed25519.Ed25519PrivateKey):
                wrapped = multicodec.wrap("ed25519-priv", value.private_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PrivateFormat.Raw,
                    encryption_algorithm=serialization.NoEncryption()
                ))
                data[key] = multibase.encode(wrapped, "base58btc")
            elif isinstance(value, rsa.RSAPublicKey):
                wrapped = multicodec.wrap("rsa-pub", value.public_bytes(
                    encoding=serialization.Encoding.DER,
                    format=serialization.PublicFormat.PKCS1
                ))
                data[key] = multibase.encode(wrapped, "base58btc")
            elif isinstance(value, ed25519.Ed25519PublicKey):
                wrapped = multicodec.wrap("ed25519-pub", value.public_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PublicFormat.Raw
                ))
                data[key] = multibase.encode(wrapped, "base58btc")
            else:
                data[key] = value
        data.update(extra)
        return data