import asyncio
from os import getenv
from dotenv import load_dotenv
from api.bot import Command
from api.bot.types import Message, Button
from api.aiogram import AiogramBot

load_dotenv()

class StartCommand(Command):
    async def handle(self, message: Message, bot: AiogramBot):
        keyboard = bot.keyboard_factory().create_inline_keyboard()
        keyboard.add_row(Button('Кнопка 1', 'btn1'), Button('Кнопка 2', 'btn2')).add_row(Button('Кнопка снизу', 'btn3'))

        await bot.send_message(message.sender_id, 'Hello, this is a /start command implementation', keyboard)
    
    def aliases(self):
        return [ 'start' ]

bot = AiogramBot(getenv('TOKEN'))

async def main():
    await bot.register_command(StartCommand())
    await bot.start()

if __name__ == '__main__':
    asyncio.run(main())
