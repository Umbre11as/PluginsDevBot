import asyncio
from os import getenv
from dotenv import load_dotenv
from api.bot import Command
from api.bot.types import Message
from api.aiogram import AiogramBot

load_dotenv()

class StartCommand(Command):
    async def handle(self, message: Message, bot):
        await bot.send_message(message.sender_id, 'Hello, this is a /start command implementation')
    
    def aliases(self):
        return [ 'start' ]

bot = AiogramBot(getenv('TOKEN'))

async def main():
    await bot.register_command(StartCommand())
    await bot.start()

if __name__ == '__main__':
    asyncio.run(main())
