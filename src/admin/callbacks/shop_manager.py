from api.bot.command import TextHandler
from keyboard import KeyboardManager
from shop import ShopRepository
from configs import Messages

class AdminShopTextHandler(TextHandler):
    def __init__(self, messages: Messages, shop: ShopRepository, keyboard_manager: KeyboardManager):
        self.messages = messages
        self.shop = shop
        self.keyboard_manager = keyboard_manager

    async def handle(self, message, bot):
        plugins = self.shop.list_plugins()
        if len(plugins) == 0:
            await bot.send_message(message.sender_id, self.messages.shop.empty, parse_mode='HTML')
            return

        keyboard = self.keyboard_manager.create_plugins_keyboard(plugins)

        await bot.send_message(message.sender_id, self.messages.admin.shop.welcome, parse_mode='HTML', keyboard=keyboard)

    def pattern(self):
        return self.messages.admin.keyboard.shop
