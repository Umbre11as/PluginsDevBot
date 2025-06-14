from ....bot.command.text import TextManager
from ..util import Adapter
import aiogram
import re

class AiogramTextManager(TextManager):
    def __init__(self, bot, dispatcher: aiogram.Dispatcher):
        super().__init__(bot)
        self.dispatcher = dispatcher
    
    def setup_handlers(self):
        @self.dispatcher.message()
        async def text_handler(message: aiogram.types.Message):
            if message.text and not message.text.startswith('/'):
                converted_message = Adapter.to_message(message)
                
                for handler in self.handlers:
                    if self.matches_pattern(converted_message.text, handler.pattern()):
                        await handler.handle(converted_message, self.bot)
    
    def matches_pattern(self, text: str, pattern: str) -> bool:
        if '*' in pattern:
            regex_pattern = pattern.replace('*', '.*')
            return bool(re.match(f'^{regex_pattern}$', text))
        
        return text == pattern
