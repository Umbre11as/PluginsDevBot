from api.bot import Command
from api.bot.types import Message
from configs import Messages
from admin.wait import PasswordWaitStates

class AdminCommand(Command):
    def __init__(self, messages: Messages):
        super().__init__()
        self.messages = messages

    async def handle(self, message: Message, bot):
        user_id = message.sender_id
        if user_id in PasswordWaitStates.failed_attempts and PasswordWaitStates.failed_attempts[user_id] >= 3:
            await bot.send_message(user_id, self.messages.admin.blocked, parse_mode='HTML')
            return
        
        PasswordWaitStates.waiting_for_password[user_id] = True
        await bot.send_message(user_id, self.messages.admin.enter_password, parse_mode='HTML')
    
    def aliases(self):
        return [ 'admin' ]
