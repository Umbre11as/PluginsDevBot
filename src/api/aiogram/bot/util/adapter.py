import aiogram.types
from api.bot import types
from api.bot.types import Document

class Adapter:
    @staticmethod
    def to_message(message: aiogram.types.Message) -> types.Message:
        document = None
        if message.document:
            document = Document(
                file_id=message.document.file_id,
                file_name=message.document.file_name,
                mime_type=message.document.mime_type,
                file_size=message.document.file_size
            )
        
        return types.Message(
            sender_id=message.from_user.id,
            text=message.text or '',
            document=document
        )

    @staticmethod
    def to_callback_query(callback: aiogram.types.CallbackQuery) -> types.CallbackQuery:
        return types.CallbackQuery(
            id=callback.id,
            from_user_id=callback.from_user.id,
            data=callback.data,
            message_id=callback.message.message_id if callback.message else 0
        )
