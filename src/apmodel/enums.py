import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from enum import Enum
    
    class StrEnum(str, Enum):
        """
        Enum where members are also (and must be) strings
        """
        
        def __str__(self) -> str:
            return str(self.value)
        
class Visibility(StrEnum):
    PUBLIC = "https://www.w3.org/ns/activitystreams#Public"
    
