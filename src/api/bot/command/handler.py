from abc import ABC, abstractmethod
from .base import Command

class CommandHandler(ABC):
    def __init__(self, bot):
        self.bot = bot

    @abstractmethod
    def register(self, command: Command):
        raise NotImplementedError()
