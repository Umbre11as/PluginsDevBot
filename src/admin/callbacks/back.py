from api.bot.command.text import TextHandler
from configs import Messages
from keyboard import KeyboardManager

class AdminBackTextHandler(TextHandler):
    def __init__(self, messages: Messages, keyboard_manager: KeyboardManager):
        self.messages = messages
        self.keyboard_manager = keyboard_manager
    
    async def handle(self, message, bot):
        await bot.send_message(message.sender_id, '\n'.join(self.messages.start), keyboard=self.keyboard_manager.create_main_keyboard(), parse_mode='HTML')
    
    def pattern(self):
        return self.messages.admin.keyboard.back
