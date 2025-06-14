import aiogram
from ....bot import types

class Adapter:
    @staticmethod
    def to_message(message: aiogram.types.Message) -> types.Message:
        return types.Message(message.from_user.id, message.text)

    @staticmethod
    def to_callback_query(callback: aiogram.types.CallbackQuery) -> types.CallbackQuery:
        return types.CallbackQuery(callback.id, callback.from_user.id, callback.data, callback.message.message_id if callback.message else 0)
