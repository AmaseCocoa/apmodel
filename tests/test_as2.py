import glob
import json
import os
from typing import Literal

import pytest

import apmodel
from apmodel.core import Link as AS2Link
from apmodel.core import Object as AS2Object
from apmodel.loader import type_loader

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CORE_PATTERN = os.path.join(
    BASE_DIR, "vendor/activitystreams/test/core-*-jsonld.json"
)
VOCAB_PATTERN = os.path.join(
    BASE_DIR, "vendor/activitystreams/test/vocabulary-*-jsonld.json"
)

CORE_JSON_FILES = glob.glob(CORE_PATTERN)
VOCAB_JSON_FILES = glob.glob(VOCAB_PATTERN)


class Activity(AS2Link):
    type: Literal["Activity"] = "Activity"


class Object(AS2Object):
    type: Literal["Object"] = "Object"


class Link(AS2Link):
    type: Literal["Link"] = "Link"


type_loader.set("https://www.w3.org/ns/activitystreams#Activity", Activity)
type_loader.set("https://www.w3.org/ns/activitystreams#Object", Object)
type_loader.set("https://www.w3.org/ns/activitystreams#Link", Link)


def normalize_as2_types(data: dict) -> dict:
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            if k == "type" and isinstance(v, list):
                new_dict[k] = v[0]
            else:
                new_dict[k] = normalize_as2_types(v)
        return new_dict
    return data

@pytest.mark.parametrize(
    "filepath",
    CORE_JSON_FILES,
    ids=[os.path.basename(f) for f in CORE_JSON_FILES],
)
def test_vendor_json_files(filepath: str):
    filename = os.path.basename(filepath)

    with open(filepath, encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON Format: {filename}")

    if not data.get("type"):
        pytest.skip()

    normalized = normalize_as2_types(data)
    type = type_loader.tjld.resolve(normalized)
    if type and type.startswith("https://www.w3.org/ns/activitystreams"):
        model = apmodel.load(normalized)

        assert model
        assert hasattr(model, "type")
        assert model.type == normalized["type"]
        assert data is not None
    else:
        pytest.skip()

@pytest.mark.parametrize(
    "filepath",
    VOCAB_JSON_FILES,
    ids=[os.path.basename(f) for f in VOCAB_JSON_FILES],
)
def test_vendor_json_files_vocab(filepath: str):
    filename = os.path.basename(filepath)

    with open(filepath, encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.skip(f"Invalid JSON Format: {filename}")

    if not data.get("type"):
        pytest.skip()

    normalized = normalize_as2_types(data)
    type = type_loader.tjld.resolve(normalized)
    if type and type.startswith("https://www.w3.org/ns/activitystreams"):
        if isinstance(normalized.get("actor"), list):
            normalized["actor"] = normalized["actor"][1]
        if isinstance(normalized.get("object"), list):
            normalized["object"] = normalized["object"][1]
        model = apmodel.load(normalized)

        assert model
        assert hasattr(model, "type")
        assert model.type == normalized["type"]
        assert data is not None
    else:
        pytest.skip()
