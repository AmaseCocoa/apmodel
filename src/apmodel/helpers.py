from typing import Dict, Any, List, Set

def has_match(data: Dict[str, Any], expected_keys: List[str]) -> bool:
    expected_keys_set: Set[str] = set(expected_keys)

    current_keys_set: Set[str] = set(data.keys())
    
    if current_keys_set == expected_keys_set:
        return True
    else:
        return False