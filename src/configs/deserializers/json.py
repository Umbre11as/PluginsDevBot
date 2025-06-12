import json
from typing import Any, Type
from pathlib import Path

from ..core.file import FileDeserializer, FileNotFoundError
from .base import BaseDeserializer, DeserializationError

class JsonDeserializer(BaseDeserializer, FileDeserializer):
    def __init__(self, path: str):
        FileDeserializer.__init__(self, path)

    def deserialize(self, cls: Type[Any], data: Any = None) -> Any:
        if data is None:
            return self.load(cls)
        return super().deserialize(cls, data)

    def load(self, cls: Type[Any]) -> Any:
        try:
            path = Path(self.path)
            if not path.exists():
                raise FileNotFoundError(f'File not found: {self.path}')
            
            content = path.read_text(encoding='utf-8')
            data = json.loads(content)
            return super().deserialize(cls, data)
        except json.JSONDecodeError as e:
            raise DeserializationError(f'Invalid JSON: {e}')
        except Exception as e:
            raise DeserializationError(f'Failed to load JSON file: {e}')
