from ....bot.keyboard import CallbackManager
from ..util import Adapter
import aiogram
import re

class AiogramCallbackManager(CallbackManager):
    def __init__(self, bot, dispatcher: aiogram.Dispatcher):
        super().__init__(bot)
        self.dispatcher = dispatcher
    
    def setup_handlers(self):
        @self.dispatcher.callback_query()
        async def callback_handler(callback: aiogram.types.CallbackQuery):
            converted_callback = Adapter.to_callback_query(callback)
            
            for handler in self.handlers:
                if self.matches_pattern(converted_callback.data, handler.pattern()):
                    await handler.handle(converted_callback, self.bot)
                    await callback.answer()
                    
                    break
    
    def matches_pattern(self, data: str, pattern: str) -> bool:
        if '*' in pattern:
            regex_pattern = pattern.replace('*', '.*')
            return bool(re.match(f'^{regex_pattern}$', data))

        return data == pattern
