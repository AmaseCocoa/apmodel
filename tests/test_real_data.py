import json
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

import apmodel
from apmodel.extra.schema.propertyvalue import PropertyValue
from apmodel.vocab.activity.create import Create
from apmodel.vocab.actor import ActorEndpoints, Person
from apmodel.vocab.note import Note


@pytest.fixture
def test_data_path(request) -> Path:
    return Path(request.path.parent) / "data"


def test_misskey_person(test_data_path: Path):
    data_loc = test_data_path / "misskey_actor.json"
    with open(data_loc, "r") as f:
        actor_dict = json.load(f)
        actor = apmodel.load(actor_dict)

        assert isinstance(actor, Person)
        assert actor.id == "https://misskey.example.com/users/afm74io04yxx0000"
        assert actor.preferred_username == "user"
        assert actor.name == "User"
        assert actor.summary == "<p>Hello</p>"
        assert isinstance(actor.endpoints, ActorEndpoints)

        assert isinstance(actor.attachment[0], PropertyValue)

        # check extra value
        assert actor._misskey_summary == "Hello"

        # check apmodel methods
        assert isinstance(actor.public_key.public_key, RSAPublicKey)


def test_misskey_activity(test_data_path: Path):
    data_loc = test_data_path / "misskey_activity.json"
    with open(data_loc, "r") as f:
        activity_dict = json.load(f)
        activity = apmodel.load(activity_dict)

        assert isinstance(activity, Create)
        assert (
            activity.id
            == "https://misskey.example.com/notes/ag8g1pmyifww004j/activity"
        )
        assert (
            activity.actor
            == "https://misskey.example.com/users/afm74io04yxx0000"
        )
        assert activity.published == "2025-12-13T22:40:41.482Z"
        assert isinstance(activity.object, Note)
        assert activity.object.id == "https://misskey.example.com/notes/ag8g1pmyifww004j"
        assert activity.object.attributed_to == "https://misskey.example.com/users/afm74io04yxx0000"
        assert activity.object.content == "This is a main content"


        # check extra value

        # check apmodel methods


# Fedibird / Mastodon 3.x
def test_fedibird_person(test_data_path: Path):
    data_loc = test_data_path / "fedibird_actor.json"
    with open(data_loc, "r") as f:
        actor_dict = json.load(f)
        actor = apmodel.load(actor_dict)

        assert isinstance(actor, Person)
        assert actor.id == "https://fedibird.example.com/users/user"
        assert actor.preferred_username == "user"
        assert actor.name == "User"
        assert actor.summary == "<p>Hello</p>"
        assert isinstance(actor.endpoints, ActorEndpoints)
        assert isinstance(actor.attachment[0], PropertyValue)

        # check extra value
        assert actor.model_extra.get("vcard:Address") == "Earth"
        assert isinstance(actor.otherSetting, list)
        assert (
            isinstance(actor.searchableBy, list)
            and actor.searchableBy[0] == "https://fedibird.example.com/users/user"
        )

        # check apmodel methods
        assert isinstance(actor.public_key.public_key, RSAPublicKey)


def test_akkoma_actor(test_data_path: Path):
    data_loc = test_data_path / "akkoma_actor.json"
    with open(data_loc, "r") as f:
        actor_dict = json.load(f)
        actor = apmodel.load(actor_dict)

        assert isinstance(actor, Person)
        assert actor.id == "https://akkoma.example.com/users/user"
        assert actor.preferred_username == "user"
        assert actor.name == "User"
        assert actor.summary == "Hello"
        assert isinstance(actor.endpoints, ActorEndpoints)
        assert actor.endpoints.oauthAuthorizationEndpoint == "https://akkoma.example.com/oauth/authorize"


def test_akkoma_note(test_data_path: Path):
    data_loc = test_data_path / "akkoma_note.json"
    with open(data_loc, "r") as f:
        note_dict = json.load(f)
        note = apmodel.load(note_dict)

        assert isinstance(note, Note)
        assert note.id == "https://akkoma.example.com/objects/bcd39b5c-004f-4897-81b1-2b7a4caa398b"
        assert note.sensitive is True
        assert note.summary == "test"
        assert note.content == "<p>:blobthumbsup: 👀</p>"


def test_akkoma_replies(test_data_path: Path):
    from apmodel.core.collection import OrderedCollection
    data_loc = test_data_path / "akkoma_replies.json"
    with open(data_loc, "r") as f:
        replies_dict = json.load(f)
        replies = apmodel.load(replies_dict)

        assert isinstance(replies, OrderedCollection)
        assert replies.total_items == 1
        assert replies.first is not None
        assert replies.first.type == "OrderedCollectionPage"

