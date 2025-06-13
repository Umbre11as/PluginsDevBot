from abc import ABC, abstractmethod
from .types.keyboard import InlineKeyboard, ReplyKeyboard

class KeyboardFactory(ABC):
    @abstractmethod
    def create_inline_keyboard(self) -> InlineKeyboard:
        raise NotImplementedError()
    
    @abstractmethod
    def create_reply_keyboard(self, resize_keyboard: bool = True, one_time_keyboard: bool = False) -> ReplyKeyboard:
        raise NotImplementedError()
