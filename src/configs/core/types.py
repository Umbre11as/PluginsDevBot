from enum import Enum, auto
from typing import Union, Dict, List, Any

class ConfigFormat(Enum):
    YAML = auto(),
    JSON = auto(),

ConfigData = Union[Dict[str, Any], List[Any], str, int, float, bool, None]
