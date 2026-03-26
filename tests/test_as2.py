from apmodel.wrapper import WrapAS2
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
TARGET_PATTERN = os.path.join(
    BASE_DIR, "vendor/activitystreams/test/*-jsonld.json"
)

JSON_FILES = glob.glob(TARGET_PATTERN)


class Object(AS2Object):
    type: Literal["Object"] = "Object"


class Link(AS2Link):
    type: Literal["Link"] = "Link"


type_loader.set("https://www.w3.org/ns/activitystreams#Object", Object)
type_loader.set("https://www.w3.org/ns/activitystreams#Link", Link)


@pytest.mark.parametrize(
    "filepath", JSON_FILES, ids=[os.path.basename(f) for f in JSON_FILES]
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

    model = apmodel.load(data)

    assert model
    assert hasattr(model, "type")
    assert model.type == data["type"]
    assert data is not None
