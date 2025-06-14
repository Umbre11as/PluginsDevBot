from api.bot.keyboard import Button
from api.bot.keyboard_factory import KeyboardFactory
from configs import Messages

class KeyboardManager:
    def __init__(self, keyboard_factory: KeyboardFactory, messages: Messages):
        self.keyboard_factory = keyboard_factory
        self.messages = messages

    def create_main_keyboard(self):
        keyboard = self.keyboard_factory.create_reply_keyboard()
        
        keyboard.add_row(Button(self.messages.keyboard.make_order))
        keyboard.add_row(Button(self.messages.keyboard.shop))
        keyboard.add_row(
            Button(self.messages.keyboard.support),
            Button(self.messages.keyboard.my_orders),
        )
        return keyboard

    def create_admin_keyboard(self):
        keyboard = self.keyboard_factory.create_reply_keyboard()

        keyboard.add_row(Button(self.messages.admin.shop))
        keyboard.add_row(Button(self.messages.admin.orders))
        keyboard.add_row(Button(self.messages.admin.back))
        return keyboard
