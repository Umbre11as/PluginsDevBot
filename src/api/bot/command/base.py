from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING
from ..types import Message

if TYPE_CHECKING:
    from ...bot import Bot

class Command(ABC):
    @abstractmethod
    async def handle(self, message: Message, bot: 'Bot'):
        raise NotImplementedError()

    @abstractmethod
    def aliases(self) -> List[str]:
        raise NotImplementedError()
