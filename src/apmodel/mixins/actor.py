from typing import Protocol

from apmodel.cid import Multikey
from apmodel.security import CryptographicKey


class ActorFieldsProtocol(Protocol):
    public_key: CryptographicKey
    assertion_method: list[Multikey]


class ActorMixin:
    @property
    def keys(self: ActorFieldsProtocol) -> list[CryptographicKey | Multikey]:
        """
        Provides a unified list of all keys associated with the actor.

        This property combines `public_key` and `assertion_method` into a single
        list for easier access.

        Returns:
            A list containing CryptographicKey and/or Multikey objects.
        """
        ret: list[Multikey | CryptographicKey] = []
        if self.public_key:
            ret.append(self.public_key)
        ret.extend(self.assertion_method)
        return ret

    def get_key(self, key_id: str) -> CryptographicKey | Multikey | None:
        """
        Finds a key by its ID from all keys associated with the actor.

        Args:
            key_id: The ID of the key to find.

        Returns:
            The key object (CryptographicKey or Multikey) if found,
            otherwise None.
        """
        return next((key for key in self.keys if key.id == key_id), None)
