import sys
from typing import Dict


class TypeInferencer:
    def __init__(self) -> None:
        self.__type_mapping: Dict[str, type] = {}
        
    def get(self, name: str) -> type | None:
        return self.__type_mapping.get(sys.intern(name))