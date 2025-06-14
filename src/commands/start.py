from api.bot import Command
from api.bot.types import Message
from configs import Messages
from keyboard import KeyboardManager

class StartCommand(Command):
    def __init__(self, messages: Messages, keyboard_manager: KeyboardManager):
        super().__init__()
        self.messages = messages
        self.keyboard_manager = keyboard_manager

    async def handle(self, message: Message, bot):
        await bot.send_message(message.sender_id, '\n'.join(self.messages.start), keyboard=self.keyboard_manager.create_main_keyboard(), parse_mode='html')
    
    def aliases(self):
        return [ 'start' ]
