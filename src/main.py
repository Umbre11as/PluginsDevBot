import asyncio
from os import getenv
from dotenv import load_dotenv
from api.configs import ConfigurationManager
from api.bot import Command
from api.bot.types import Message
from api.bot.keyboard import Button, CallbackHandler, CallbackQuery
from api.aiogram import AiogramBot
import configs

load_dotenv()

manager = ConfigurationManager('configs')
messages = manager.load(configs.Messages, 'messages.yml')

class StartCommand(Command):
    async def handle(self, message: Message, bot: AiogramBot):
        keyboard = bot.keyboard_factory().create_reply_keyboard()
        keyboard.add_row(Button(messages.keyboard.make_order, 'main_make_order'))
        keyboard.add_row(Button(messages.keyboard.shop, 'main_shop'))
        keyboard.add_row(
            Button(messages.keyboard.support, 'main_support'),
            Button(messages.keyboard.my_orders, 'main_my_orders'),
        )

        await bot.send_message(message.sender_id, '\n'.join(messages.start), keyboard=keyboard, parse_mode='html')
    
    def aliases(self):
        return [ 'start' ]

bot = AiogramBot(getenv('TOKEN'))

async def main():
    await bot.register_command(StartCommand())

    await bot.start()

if __name__ == '__main__':
    asyncio.run(main())
