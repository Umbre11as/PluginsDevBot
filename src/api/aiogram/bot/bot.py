from ...bot import Bot
from ..bot.command import AiogramCommandHandler, Command
from ..bot.keyboard import AiogramKeyboardFactory
from ...bot.keyboard_factory import KeyboardFactory
from ...bot.types.keyboard import Keyboard
from typing import Optional
import aiogram

class AiogramBot(Bot):
    def __init__(self, token: str):
        self.telegram = aiogram.Bot(token)
        self.dispatcher = aiogram.Dispatcher()
        self.command_handler = AiogramCommandHandler(self, self.dispatcher)
        self.keyboardfactory = AiogramKeyboardFactory()

    async def register_command(self, command: Command):
        self.command_handler.register(command)

    async def send_message(self, id: int, text: str, keyboard: Optional[Keyboard] = None):
        reply_markup = None
        if keyboard:
            reply_markup = keyboard.build()
        
        await self.telegram.send_message(id, text, parse_mode='html', reply_markup=reply_markup)

    def keyboard_factory(self) -> KeyboardFactory:
        return self.keyboardfactory

    async def start(self):
        await super().start()
        await self.dispatcher.start_polling(self.telegram)
