import json
from datetime import datetime
from typing import Union

from pyld import jsonld


def map_jsonld_type_to_python(jsonld_type):
    type_mapping = {
        "http://www.w3.org/2001/XMLSchema#string": str,
        "http://www.w3.org/2001/XMLSchema#integer": int,
        "http://www.w3.org/2001/XMLSchema#boolean": bool,
        "http://www.w3.org/2001/XMLSchema#float": float,
        "http://www.w3.org/2001/XMLSchema#double": float,
        "http://www.w3.org/2001/XMLSchema#dateTime": datetime,
    }
    return type_mapping.get(jsonld_type, str)

def infer_literal_type(value):
    if isinstance(value, bool):  
        return bool  
    elif isinstance(value, int):  
        return int  
    elif isinstance(value, float):  
        return float  
    elif isinstance(value, str):
        try:  
            datetime.fromisoformat(value.replace('Z', '+00:00'))  
            return datetime  
        except ValueError:  
            try:  
                if '.' in value:  
                    return float  
                else:  
                    return int  
            except ValueError:  
                return str  
    else:  
        return str

def extract_property_type(values):
    """展開されたJSON-LD値からPython/Pydanticの型を抽出"""
    if not isinstance(values, list):
        values = [values]

    types = set()
    for value in values:
        if isinstance(value, dict):
            if "@value" in value:
                if "@type" in value:
                    types.add(map_jsonld_type_to_python(value["@type"]))
                elif "@language" in value:
                    types.add(str)
                else:
                    types.add(infer_literal_type(value["@value"]))
            elif "@id" in value:
                types.add(str)
        else:
            types.add(type(value))

    if len(types) == 1:
        return types.pop()
    else:
        return Union[tuple(sorted(types, key=lambda x: x.__name__))]


def extract_type_info(expanded_doc):
    types = {}
    for item in expanded_doc:
        if "@type" in item:
            type_name = item["@type"][0]["@id"]
            properties = {}
            for key, values in item.items():
                if key not in ["@type", "@id"]:
                    properties[key] = extract_property_type(values)
            types[type_name] = properties
    return types


with open("as2.jsonld", "r") as f:
    context_json = json.load(f)

expanded_schema = jsonld.expand(context_json)

type_info = extract_type_info(expanded_schema)
print(type_info)