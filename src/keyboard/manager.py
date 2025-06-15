from api.bot.keyboard import Button
from api.bot.keyboard_factory import KeyboardFactory
from api.placeholder import Placeholder
from shop import Plugin
from configs import Messages
from typing import List

class KeyboardManager:
    def __init__(self, keyboard_factory: KeyboardFactory, messages: Messages):
        self.keyboard_factory = keyboard_factory
        self.messages = messages

    def create_main_keyboard(self):
        keyboard = self.keyboard_factory.create_reply_keyboard()
        keyboard_settings = self.messages.keyboard
        
        keyboard.add_row(Button(keyboard_settings.make_order))
        keyboard.add_row(Button(keyboard_settings.shop))
        keyboard.add_row(
            Button(keyboard_settings.support),
            Button(keyboard_settings.my_orders),
        )
        return keyboard

    def create_admin_keyboard(self):
        keyboard = self.keyboard_factory.create_reply_keyboard()
        keyboard_settings = self.messages.admin.keyboard

        keyboard.add_row(Button(keyboard_settings.shop))
        keyboard.add_row(Button(keyboard_settings.orders))
        keyboard.add_row(Button(keyboard_settings.back))
        return keyboard

    def create_plugins_keyboard(self, plugins: List[Plugin]):
        keyboard = self.keyboard_factory.create_inline_keyboard()
        for plugin in plugins:
            text = Placeholder(self.messages.shop.button) \
                .place('{name}', plugin.name) \
                .place('{price}', str(plugin.price)) \
                .build()
            keyboard.add_button(text, f'plugin_{plugin.name}')

        return keyboard
