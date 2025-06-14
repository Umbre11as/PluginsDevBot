from abc import ABC, abstractmethod
from ..types import CallbackQuery

class CallbackHandler(ABC):
    @abstractmethod
    async def handle(self, callback: CallbackQuery, bot):
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
