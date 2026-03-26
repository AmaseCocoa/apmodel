import glob
import json
import os

import pytest

import apmodel

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_PATTERN = os.path.join(BASE_DIR, "vendor/activitystreams/test/*.json")

JSON_FILES = glob.glob(TARGET_PATTERN)


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
