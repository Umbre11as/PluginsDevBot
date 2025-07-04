from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from ..types import CallbackQuery

if TYPE_CHECKING:
    from ...bot import Bot

class CallbackHandler(ABC):
    @abstractmethod
    async def handle(self, callback: CallbackQuery, bot: 'Bot'):
        raise NotImplementedError()
    
    @abstractmethod
    def pattern(self) -> str:
        raise NotImplementedError()

class CallbackManager(ABC):
    def __init__(self, bot):
        self.bot = bot
        self.handlers = []
    
    def register(self, handler: CallbackHandler):
        self.handlers.append(handler)
    
    @abstractmethod
    def setup_handlers(self):
        raise NotImplementedError()
