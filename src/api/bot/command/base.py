from abc import ABC, abstractmethod
from typing import List
from ..types import Message
from ...bot import Bot

class Command(ABC):
    @abstractmethod
    def handle(self, message: Message, bot: Bot):
        raise NotImplementedError()

    @abstractmethod
    def aliases(self) -> List[str]:
        raise NotImplementedError()
