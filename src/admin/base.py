from api.bot.command.text import TextHandler
from api.bot.keyboard import CallbackHandler
from admin.wait import WaitStates
from configs import Messages

class AdminTextHandler(TextHandler):
    def __init__(self, messages: Messages, *args, **kwargs):
        self.messages = messages

    async def handle(self, message, bot):
        if not WaitStates.is_admin(message.sender_id):
            return
        
        await self.handle_admin(message, bot)

    async def handle_admin(self, message, bot):
        raise NotImplementedError()

class AdminCallbackHandler(CallbackHandler):
    def __init__(self, messages: Messages, *args, **kwargs):
        self.messages = messages

    async def handle(self, callback, bot):
        if not WaitStates.is_admin(callback.from_user_id):
            return
        
        await self.handle_admin(callback, bot)

    async def handle_admin(self, callback, bot):
        raise NotImplementedError()
