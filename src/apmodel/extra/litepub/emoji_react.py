from typing import ClassVar

from ...vocab.activity.like import Like


class EmojiReact(Like):
    _model_type: ClassVar[str] = "http://litepub.social/ns#EmojiReact"
    content: str