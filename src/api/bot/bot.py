from abc import ABC, abstractmethod
from log import get_logger
from .keyboard_factory import KeyboardFactory
from .keyboard import Keyboard, CallbackHandler
from typing import Optional

class Bot(ABC):
    @abstractmethod
    async def send_message(self, id: int, text: str, keyboard: Optional[Keyboard] = None):
        raise NotImplementedError()
    
    @abstractmethod
    async def edit_message(self, user_id: int, message_id: int, text: str, keyboard: Optional[Keyboard] = None):
        raise NotImplementedError()

    @abstractmethod
    def keyboard_factory(self) -> KeyboardFactory:
        raise NotImplementedError()

    @abstractmethod
    async def answer_callback(self, callback_id: str, text: str = '', show_alert: bool = False):
        raise NotImplementedError()

    @abstractmethod
    async def register_callback_handler(self, handler: CallbackHandler):
        raise NotImplementedError()

    async def start(self):
        get_logger().info('Starting bot')
