from abc import ABC, abstractmethod
from .base import Command
from ..types import Message
from ..bot import Bot

class CommandHandler(ABC):
    def __init__(self, bot: Bot):
        self.bot = bot

    @abstractmethod
    def handle_command(self, message: Message):
        raise NotImplementedError()

    @abstractmethod
    def register(self, command: Command):
        raise NotImplementedError()
