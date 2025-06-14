from api.bot import Command
from api.bot.types import Message
from api.bot.keyboard import Button
from configs import Messages

class StartCommand(Command):
    def __init__(self, messages: Messages):
        super().__init__()
        self.messages = messages

    async def handle(self, message: Message, bot):
        keyboard = bot.keyboard_factory().create_reply_keyboard()
        keyboard.add_row(Button(self.messages.keyboard.make_order, 'main_make_order'))
        keyboard.add_row(Button(self.messages.keyboard.shop, 'main_shop'))
        keyboard.add_row(
            Button(self.messages.keyboard.support, 'main_support'),
            Button(self.messages.keyboard.my_orders, 'main_my_orders'),
        )

        await bot.send_message(message.sender_id, '\n'.join(self.messages.start), keyboard=keyboard, parse_mode='html')
    
    def aliases(self):
        return [ 'start' ]
