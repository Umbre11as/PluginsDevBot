from abc import ABC, abstractmethod
from typing import Any, Type

class Serializer(ABC):
    @abstractmethod
    def serialize(self, obj: Any) -> Any:
        pass

class Deserializer(ABC):
    @abstractmethod
    def deserialize(self, cls: Type[Any], data: Any) -> Any:
        pass
