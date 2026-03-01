from __future__ import annotations

from typing import Any

from ...core.base import AS2Base


class Object(AS2Base):
    @property
    def id(self) -> Any:
        return self._get_prop("id")

    @id.setter
    def id(self, value: Any):
        self._data["id"] = value

    @property
    def type(self) -> Any:
        return self._get_prop("type")

    @type.setter
    def type(self, value: Any):
        self._data["type"] = value

    @property
    def name(self) -> Any:
        return self._get_prop("name")

    @name.setter
    def name(self, value: Any):
        self._data["name"] = value

    @property
    def attachment(self) -> Any:
        return self._get_prop("attachment")

    @attachment.setter
    def attachment(self, value: Any):
        self._data["attachment"] = value

    @property
    def attributed_to(self) -> Any:
        return self._get_prop("attributedTo")

    @attributed_to.setter
    def attributed_to(self, value: Any):
        self._data["attributedTo"] = value

    @property
    def url(self) -> Any:
        return self._get_prop("url")

    @url.setter
    def url(self, value: Any):
        self._data["url"] = value


class Note(Object):
    @property
    def content(self) -> Any:
        return self._get_prop("content")

    @content.setter
    def content(self, value: Any):
        self._data["content"] = value

    @property
    def in_reply_to(self) -> Any:
        return self._get_prop("inReplyTo")

    @in_reply_to.setter
    def in_reply_to(self, value: Any):
        self._data["inReplyTo"] = value


class Activity(Object):
    @property
    def actor(self) -> Any:
        return self._get_prop("actor")

    @actor.setter
    def actor(self, value: Any):
        self._data["actor"] = value

    @property
    def object(self) -> Any:
        return self._get_prop("object")

    @object.setter
    def object(self, value: Any):
        self._data["object"] = value

    @property
    def target(self) -> Any:
        return self._get_prop("target")

    @target.setter
    def target(self, value: Any):
        self._data["target"] = value


class Create(Activity):
    pass


class Person(Object):
    @property
    def preferred_username(self) -> Any:
        return self._get_prop("preferredUsername")

    @preferred_username.setter
    def preferred_username(self, value: Any):
        self._data["preferredUsername"] = value

    @property
    def inbox(self) -> Any:
        return self._get_prop("inbox")

    @inbox.setter
    def inbox(self, value: Any):
        self._data["inbox"] = value

    @property
    def outbox(self) -> Any:
        return self._get_prop("outbox")

    @outbox.setter
    def outbox(self, value: Any):
        self._data["outbox"] = value

    @property
    def public_key(self) -> Any:
        return self._get_prop("publicKey")

    @public_key.setter
    def public_key(self, value: Any):
        self._data["publicKey"] = value
