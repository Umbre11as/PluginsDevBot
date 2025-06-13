import asyncio
from os import getenv
from dotenv import load_dotenv
from api.aiogram import AiogramBot

load_dotenv()

bot = AiogramBot(getenv('TOKEN'))

async def main():
    await bot.start()

if __name__ == '__main__':
    asyncio.run(main())
