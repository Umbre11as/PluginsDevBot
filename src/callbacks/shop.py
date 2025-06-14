from api.bot.command.text import TextHandler
from configs import Messages

class ShopTextHandler(TextHandler):
    def __init__(self, messages: Messages):
        self.messages = messages
    
    async def handle(self, message, bot):
        plugins = bot.shop.list_plugins()
        if len(plugins) == 0:
            await bot.send_message(message.sender_id, bot.messages.shop.empty, parse_mode='HTML')
            return
        
    
    def pattern(self):
        return self.messages.keyboard.shop
