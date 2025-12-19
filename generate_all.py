import json

from apmodel.vocab.actor import Person


def trace_pydantic_recursion(obj, path="Person", memo=None):
    if memo is None:
        memo = set()

    # オブジェクト（特にリストやモデル）の識別子を確認
    obj_id = id(obj)
    if obj_id in memo:
        print(f"FOUND LOOP: {path} (Type: {type(obj)})")
        return True

    memo.add(obj_id)

    try:
        if isinstance(obj, list):
            for i, item in enumerate(obj):
                if trace_pydantic_recursion(item, f"{path}[{i}]", memo.copy()):
                    return True
        elif hasattr(obj, "model_fields"):  # Pydanticモデル判定
            # model_dump()を試行してどこで止まるか見る
            for field_name in obj.model_fields.keys():
                val = getattr(obj, field_name)
                if trace_pydantic_recursion(
                    val, f"{path}.{field_name}", memo.copy()
                ):
                    return True
    except Exception as e:
        print(f"Error at {path}: {e}")

    return False


def test_misskey_person():
    data_loc = "./tests/data/misskey_actor.json"
    with open(data_loc, "r") as f:
        actor_dict = json.load(f)
        actor = Person.model_validate(actor_dict)

    actor.model_dump()


test_misskey_person()
