import asyncio
from os import getenv
from dotenv import load_dotenv
from api.bot.payment.yoomoney import YooMoneyProvider
from bot import PluginsDevBot

load_dotenv()

yoomoney_provider = YooMoneyProvider(getenv('YOOMONEY_WALLET'), getenv('YOOMONEY_SECRET'))
bot = PluginsDevBot(getenv('TOKEN'), yoomoney_provider)

async def main():
    await bot.start()

if __name__ == '__main__':
    asyncio.run(main())
