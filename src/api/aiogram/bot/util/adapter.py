import aiogram
from ....bot import types

class Adapter:
    @staticmethod
    def to_message(message: aiogram.types.Message) -> types.Message:
        return types.Message(message.from_user.id, message.text)
