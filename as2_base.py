import datetime
import typing

import requests


def generate_as2_type_registry():
    url = "https://www.w3.org/ns/activitystreams"
    headers = {"Accept": "application/ld+json"}

    # JSON-LD取得
    res = requests.get(url, headers=headers)
    context = res.json().get("@context", {})

    # XSD/JSON-LD型 -> Pythonネイティブ型
    XSD_TO_PY = {
        "xsd:dateTime": datetime.datetime,
        "xsd:nonNegativeInteger": int,
        "xsd:integer": int,
        "xsd:float": float,
        "xsd:boolean": bool,
        "id": str,  # URI
        "@id": str,  # URI
    }

    registry = {}

    for key, val in context.items():
        # クラスではなくプロパティ（小文字始まり）のみ
        if isinstance(val, dict) and key and key.islower():
            # 1. 言語マップ型 (contentMap 等)
            if val.get("@container") == "@language":
                py_type = typing.Optional[typing.Dict[str, str]]

            # 2. 標準型 (単一値 | リスト | None)
            else:
                ld_type = val.get("@type", "@id")
                base = XSD_TO_PY.get(ld_type, str)
                # AS2の基本ルール: scalar or array
                py_type = typing.Optional[typing.Union[base, typing.List[base]]]

            registry[key] = py_type

    return registry


# レジストリの生成
AS2_TYPE_REGISTRY = generate_as2_type_registry()
fields = {k: (v, None) for k, v in AS2_TYPE_REGISTRY.items()}
print(fields)
