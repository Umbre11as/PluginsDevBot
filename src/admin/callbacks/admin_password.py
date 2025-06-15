from api.bot.command.text import TextHandler
from api.placeholder import Placeholder
from configs import Messages
from admin.wait import WaitStates
from keyboard import KeyboardManager

class AdminPasswordTextHandler(TextHandler):
    def __init__(self, messages: Messages, keyboard_manager: KeyboardManager, admin_password: str):
        self.messages = messages
        self.keyboard_manager = keyboard_manager
        self.admin_password = admin_password

    async def handle(self, message, bot):
        user_id = message.sender_id
        if user_id not in WaitStates.waiting_for_password:
            return
        
        if message.text.strip() == self.admin_password:
            del WaitStates.waiting_for_password[user_id]
            if user_id in WaitStates.failed_attempts:
                del WaitStates.failed_attempts[user_id]
            
            WaitStates.authorized_admins.add(user_id)
            await bot.send_message(user_id, self.messages.admin.welcome, keyboard=self.keyboard_manager.create_admin_keyboard(), parse_mode='HTML')
        else:
            failed_count = WaitStates.failed_attempts.get(user_id, 0) + 1
            WaitStates.failed_attempts[user_id] = failed_count
            
            attempts = 3 - failed_count
            if failed_count >= 3:
                attempts = 0
                del WaitStates.waiting_for_password[user_id]
            
            text = Placeholder(self.messages.admin.wrong_password) \
                .place('{attempts}', str(attempts)) \
                .build()
            await bot.send_message(user_id, text, parse_mode='HTML')
    
    def pattern(self):
        return '*'
