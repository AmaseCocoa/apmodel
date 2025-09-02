from datetime import datetime
from dataclasses import field, asdict, dataclass
from typing import List, Union

from ...context import LDContext
from ...types import ActivityPubModel, Undefined


@dataclass
class DataIntegrityProof(ActivityPubModel):
    _context: LDContext = field(
        default=LDContext(
            [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/data-integrity/v1",
            ]
        ),
        kw_only=True,
    )

    type: Union[str, Undefined] = field(default="DataIntegrityProof", kw_only=True)
    cryptosuite: str
    proofValue: str
    proofPurpose: str
    verificationMethod: str
    created: Union[str, datetime]
    _extra: dict = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.created, str):
            self.created = datetime.fromisoformat(self.created)

    def to_json(self):
        data = asdict(self)
        extra = data.pop("_extra", {})
        ctx = data.pop("_context")
        if isinstance(ctx, LDContext):
            data["@context"] = ctx.json
        else:
            data["@context"] = ctx
        for key, value in list(data.items()):
            if isinstance(value, Undefined):
                del data[key]
            elif isinstance(value, ActivityPubModel):
                data[key] = value.to_json()
            elif isinstance(value, list):
                data[key] = [
                    v.to_json() if isinstance(v, ActivityPubModel) else v for v in value
                ]
            elif key == "created":
                if isinstance(value, datetime):
                    data[key] = value.isoformat()
            else:
                data[key] = value
        data.update(extra)
        return data
