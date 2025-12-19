from typing import ClassVar, Optional

from pydantic import Field

from ...types import ActivityPubModel


class PropertyValue(ActivityPubModel):
    _model_type: ClassVar[str] = "http://schema.org#PropertyValue"

    type: Optional[str] = Field(default="PropertyValue", kw_only=True)

    name: Optional[str] = Field(default=None)
    value: Optional[str] = Field(default=None)
