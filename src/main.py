import asyncio
from os import getenv
from dotenv import load_dotenv
from api.bot.payment.yoomoney import YooMoneyProvider
from bot import PluginsDevBot

load_dotenv()

payment_provider = YooMoneyProvider(getenv('YOOMONEY_WALLET'), getenv('YOOMONEY_SECRET'))
bot = PluginsDevBot(getenv('TOKEN'), payment_provider, getenv('ADMIN_PASSWORD'))

async def main():
    await bot.start()

if __name__ == '__main__':
    asyncio.run(main())
