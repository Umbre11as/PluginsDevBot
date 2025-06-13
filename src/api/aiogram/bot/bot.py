from ...bot import Bot
import aiogram

class AiogramBot(Bot):
    def __init__(self, token: str):
        self.telegram = aiogram.Bot(token)
        self.dispatcher = aiogram.Dispatcher()

    async def send_message(self, id: int, text: str):
        self.telegram.send_message(id, text, parse_mode='html')

    async def start(self):
        await super().start()
        await self.dispatcher.start_polling(self.telegram)
