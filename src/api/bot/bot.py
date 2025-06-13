from abc import ABC, abstractmethod
from log import get_logger
from .keyboard_factory import KeyboardFactory
from .types.keyboard import Keyboard
from typing import Optional

class Bot(ABC):
    @abstractmethod
    async def send_message(self, id: int, text: str, keyboard: Optional[Keyboard] = None):
        raise NotImplementedError()

    @abstractmethod
    def keyboard_factory(self) -> KeyboardFactory:
        raise NotImplementedError()

    async def start(self):
        get_logger().info('Starting bot')
