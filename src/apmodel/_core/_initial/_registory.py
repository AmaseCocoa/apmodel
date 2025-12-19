from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...types import ActivityPubModel

_registory: dict[str, type["ActivityPubModel"]] = {}
