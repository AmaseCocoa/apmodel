import json
from pathlib import Path

import pytest

from apmodel.vocab.actor import Person


@pytest.fixture
def test_data_path(request) -> Path:
    return Path(request.path.parent) / "data"


def test_misskey_person(test_data_path: Path):
    data_loc = test_data_path / "misskey_actor.json"
    with open(data_loc, "r") as f:
        actor_dict = json.load(f)
        actor = Person.model_validate(actor_dict)