import json
from typing import Any
from pathlib import Path

from ..core.file import FileSerializer
from .base import BaseSerializer, SerializationError

class JsonSerializer(BaseSerializer, FileSerializer):
    def __init__(self, path: str, indent: int = 2):
        FileSerializer.__init__(self, path)
        self.indent = indent

    def serialize(self, obj: Any) -> str:
        try:
            data = super().serialize(obj)
            return json.dumps(data, indent=self.indent, ensure_ascii=False)
        except Exception as e:
            raise SerializationError(f'Failed to serialize to JSON: {e}')

    def save(self, obj: Any) -> None:
        try:
            serialized_data = self.serialize(obj)
            Path(self.path).write_text(serialized_data, encoding='utf-8')
        except Exception as e:
            raise SerializationError(f'Failed to save JSON file: {e}')
