from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from ..types import Message

if TYPE_CHECKING:
    from ...bot import Bot

class TextHandler(ABC):
    @abstractmethod
    async def handle(self, message: Message, bot: 'Bot'):
        raise NotImplementedError()
    
    @abstractmethod
    def pattern(self) -> str:
        raise NotImplementedError()

class TextManager(ABC):
    def __init__(self, bot):
        self.bot = bot
        self.handlers = []
    
    def register(self, handler: TextHandler):
        self.handlers.append(handler)
    
    @abstractmethod
    def setup_handlers(self):
        raise NotImplementedError()
