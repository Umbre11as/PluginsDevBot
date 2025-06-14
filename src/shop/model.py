from dataclasses import dataclass
from pathlib import Path
from typing import Union

PathUnion = Union[str, Path]

@dataclass
class Plugin:
    name: str
    description: str
    file_path: PathUnion
