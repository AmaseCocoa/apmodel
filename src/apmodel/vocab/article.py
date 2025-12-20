from typing import ClassVar, Optional

from pydantic import Field

from ..core.object import Object


class Article(Object):
    _model_type: ClassVar[str] = "https://www.w3.org/ns/activitystreams#Article"
    type: Optional[str] = Field(default="Article", kw_only=True, frozen=True)
