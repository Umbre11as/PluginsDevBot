from abc import ABC, abstractmethod
from log import get_logger

class Bot(ABC):
    @abstractmethod
    async def send_message(self, id: int, text: str):
        raise NotImplementedError()

    async def start(self):
        get_logger().info('Starting bot')
