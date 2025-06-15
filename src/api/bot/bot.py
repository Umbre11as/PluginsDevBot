from abc import ABC, abstractmethod
from api.log import get_logger
from .keyboard_factory import KeyboardFactory
from .keyboard import Keyboard, CallbackHandler
from .payment import PaymentManager
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .command.text import TextHandler

class Bot(ABC):
    @abstractmethod
    async def send_message(self, id: int, text: str, keyboard: Optional[Keyboard] = None, parse_mode='MarkdownV2'):
        raise NotImplementedError()
    
    @abstractmethod
    async def edit_message(self, user_id: int, message_id: int, text: str, keyboard: Optional[Keyboard] = None, parse_mode='MarkdownV2'):
        raise NotImplementedError()

    @abstractmethod
    async def send_document(self, user_id: int, document, caption: Optional[str] = None):
        raise NotImplementedError()
    
    @abstractmethod
    async def download_file(self, file_id: str, destination_path: str):
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
    
    @abstractmethod
    async def register_text_handler(self, handler: 'TextHandler'):
        raise NotImplementedError()

    @abstractmethod
    def payment_manager(self) -> PaymentManager:
        raise NotImplementedError()
    
    async def start(self):
        get_logger().info('Starting bot')
