from pathlib import Path
from typing import Union

from .core.types import ConfigFormat
from .serializers.json import JsonSerializer
from .serializers.yaml import YamlSerializer
from .deserializers.json import JsonDeserializer
from .deserializers.yaml import YamlDeserializer

class UnsupportedFormatError(Exception):
    pass

class ConfigFactory:
    @staticmethod
    def get_format(path: Union[str, Path]) -> ConfigFormat:
        path = Path(path)
        suffix = path.suffix.lower()
        
        if suffix in [ '.yaml', '.yml' ]:
            return ConfigFormat.YAML
        elif suffix == '.json':
            return ConfigFormat.JSON
        else:
            raise UnsupportedFormatError(f'Unsupported file format: {suffix}')

    @staticmethod
    def create_serializer(path: Union[str, Path], format: ConfigFormat = None):
        path = str(path)
        if format is None:
            format = ConfigFactory.get_format(path)
        
        if format == ConfigFormat.JSON:
            return JsonSerializer(path)
        elif format == ConfigFormat.YAML:
            return YamlSerializer(path)
        else:
            raise UnsupportedFormatError(f'Unsupported format: {format}')

    @staticmethod
    def create_deserializer(path: Union[str, Path], format: ConfigFormat = None):
        path = str(path)
        if format is None:
            format = ConfigFactory.get_format(path)
        
        if format == ConfigFormat.JSON:
            return JsonDeserializer(path)
        elif format == ConfigFormat.YAML:
            return YamlDeserializer(path)
        else:
            raise UnsupportedFormatError(f'Unsupported format: {format}')
