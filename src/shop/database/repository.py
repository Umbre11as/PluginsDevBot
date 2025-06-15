from abc import ABC, abstractmethod
from typing import List
from decimal import Decimal
from ..model import PathUnion, Plugin

class ShopRepository(ABC):
    @abstractmethod
    def add_plugin(self, name: str, description: str, file_path: PathUnion, price: Decimal):
        raise NotImplementedError()

    @abstractmethod
    def remove_plugin(self, name: str):
        raise NotImplementedError()

    @abstractmethod
    def get_plugin(self, name: str) -> Plugin:
        raise NotImplementedError()

    @abstractmethod
    def list_plugins(self) -> List[Plugin]:
        raise NotImplementedError()
