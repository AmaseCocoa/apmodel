from apmodel.base import AS2Model
from apmodel.context import Context
from apmodel.core import Object


def test_activity_pub_model_creation():
    obj = Object(id="http://example.com/obj", name="Test Object")

    assert obj.id == "http://example.com/obj"
    assert obj.name == "Test Object"


def test_activity_pub_model_dump():
    # Test the dump method
    obj = Object(id="http://example.com/obj", name="Test Object")

    dumped = obj.dump()

    assert "id" in dumped
    assert "name" in dumped
    assert dumped["id"] == "http://example.com/obj"
    assert dumped["name"] == "Test Object"


def test_activity_pub_model_serializer():
    obj = Object(id="http://example.com/obj", name="Test Object")

    serialized = obj.dump()

    assert "@context" in serialized
    assert "id" in serialized
    assert "name" in serialized
    assert serialized["id"] == "http://example.com/obj"
    assert serialized["name"] == "Test Object"


def test_activity_pub_model_with_nested_object():
    nested_obj = Object(id="http://example.com/nested", name="Nested Object")
    main_obj = Object(
        id="http://example.com/main",
        name="Main Object",
        attachment=[nested_obj],
    )

    serialized = main_obj.dump()

    assert "@context" in serialized
    assert "id" in serialized
    assert "name" in serialized
    assert "attachment" in serialized
    assert len(serialized["attachment"]) == 1
    assert serialized["attachment"][0]["id"] == "http://example.com/nested"
    assert serialized["attachment"][0]["name"] == "Nested Object"
    assert "@context" not in serialized["attachment"][0]


def test_activity_pub_model_context_aggregation():
    obj = Object(
        id="http://example.com/obj",
        name="Test Object",
        ctx=Context.parse(
            [
                "https://www.w3.org/ns/activitystreams",
                "http://example.com/custom_context",
            ]
        ),
    )

    serialized = obj.dump()

    assert "@context" in serialized
    assert "https://www.w3.org/ns/activitystreams" in serialized["@context"]
    assert "http://example.com/custom_context" in serialized["@context"]


def test_activity_pub_model_extra_fields():
    raw_obj = {
        "id": "http://example.com/obj",
        "name": "Test Object",
        "customField": "custom_value",
    }

    obj = AS2Model.model_validate(raw_obj)

    serialized = obj.model_dump(by_alias=True)

    assert "id" in serialized
    assert "name" in serialized
    assert "customField" in serialized
    assert serialized["customField"] == "custom_value"
