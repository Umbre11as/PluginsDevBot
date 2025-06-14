from .base import *

class FileNotFoundError(Exception):
    pass

class FileSerializer(Serializer):
    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def serialize(self, obj: Any) -> Any:
        pass

    @abstractmethod
    def save(self, obj: Any) -> None:
        pass

class FileDeserializer(Deserializer):
    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def deserialize(self, cls: Type[Any], data: Any = None) -> Any:
        pass

    @abstractmethod
    def load(self, cls: Type[Any]) -> Any:
        pass
