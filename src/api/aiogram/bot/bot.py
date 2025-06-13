from ...bot import Bot
from ..bot.command import AiogramCommandHandler, Command
import aiogram

class AiogramBot(Bot):
    def __init__(self, token: str):
        self.telegram = aiogram.Bot(token)
        self.dispatcher = aiogram.Dispatcher()
        self.command_handler = AiogramCommandHandler(self.telegram, self.dispatcher)

    async def register_command(self, command: Command):
        self.command_handler.register(command)

    async def send_message(self, id: int, text: str):
        self.telegram.send_message(id, text, parse_mode='html')

    async def start(self):
        await super().start()
        await self.dispatcher.start_polling(self.telegram)
