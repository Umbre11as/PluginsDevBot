from abc import ABC, abstractmethod

class Bot(ABC):
    @abstractmethod
    def send_message(id: int, text: str):
        raise NotImplementedError()
