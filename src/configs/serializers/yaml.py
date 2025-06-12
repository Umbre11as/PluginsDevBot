import yaml
from typing import Any
from pathlib import Path

from ..core.file import FileSerializer
from .base import BaseSerializer, SerializationError

class YamlSerializer(BaseSerializer, FileSerializer):
    def __init__(self, path: str):
        FileSerializer.__init__(self, path)

    def serialize(self, obj: Any) -> str:
        try:
            data = super().serialize(obj)
            return yaml.dump(data, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            raise SerializationError(f'Failed to serialize to YAML: {e}')

    def save(self, obj: Any) -> None:
        try:
            serialized_data = self.serialize(obj)
            Path(self.path).write_text(serialized_data, encoding='utf-8')
        except Exception as e:
            raise SerializationError(f'Failed to save YAML file: {e}')
