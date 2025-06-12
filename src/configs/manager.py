from pathlib import Path
from typing import Type, Any, Union, Optional

from .core.types import ConfigFormat
from .factory import ConfigFactory

class ConfigurationError(Exception):
    pass

class ConfigurationManager:
    def __init__(self, base_path: Union[str, Path] = '.'):
        self.base_path = Path(base_path)

    def load(self, cls: Type[Any], path: Union[str, Path], format: ConfigFormat = None) -> Any:
        full_path = self.base_path / path
        deserializer = ConfigFactory.create_deserializer(full_path, format)
        return deserializer.load(cls)

    def save(self, obj: Any, path: Union[str, Path], format: ConfigFormat = None) -> None:
        full_path = self.base_path / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        serializer = ConfigFactory.create_serializer(full_path, format)
        serializer.save(obj)

    def load_or_create(self, cls: Type[Any], path: Union[str, Path], 
                      default: Optional[Any] = None, format: ConfigFormat = None) -> Any:
        full_path = self.base_path / path
        
        if full_path.exists():
            return self.load(cls, path, format)
        elif default is not None:
            self.save(default, path, format)
            return default
        else:
            raise ConfigurationError(f'Config file not found and no default provided: {full_path}')

    def exists(self, path: Union[str, Path]) -> bool:
        return (self.base_path / path).exists()

    def delete(self, path: Union[str, Path]) -> None:
        full_path = self.base_path / path
        if full_path.exists():
            full_path.unlink()

    def migrate(self, obj: Any, source_path: Union[str, Path], 
                target_path: Union[str, Path], target_format: ConfigFormat = None) -> None:
        self.save(obj, target_path, target_format)
        self.delete(source_path)
