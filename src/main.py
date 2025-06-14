import asyncio
from os import getenv
from dotenv import load_dotenv
from bot import PluginsDevBot

load_dotenv()

bot = PluginsDevBot(getenv('TOKEN'))

async def main():
    await bot.start()

if __name__ == '__main__':
    asyncio.run(main())
