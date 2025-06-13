from ...bot.types.keyboard import InlineKeyboard, ReplyKeyboard, Button
from ...bot.keyboard_factory import KeyboardFactory
import aiogram.types

class AiogramInlineKeyboard(InlineKeyboard):
    def build(self) -> aiogram.types.InlineKeyboardMarkup:
        keyboard_rows = []
        for row in self.rows:
            keyboard_row = []
            for button in row.buttons:
                keyboard_row.append(aiogram.types.InlineKeyboardButton(text=button.text, callback_data=button.callback_data))
            
            keyboard_rows.append(keyboard_row)
        
        return aiogram.types.InlineKeyboardMarkup(inline_keyboard=keyboard_rows)

class AiogramReplyKeyboard(ReplyKeyboard):
    def build(self) -> aiogram.types.ReplyKeyboardMarkup:
        keyboard_rows = []
        for row in self.rows:
            keyboard_row = []
            for button in row.buttons:
                keyboard_row.append(aiogram.types.KeyboardButton(text=button.text))
            
            keyboard_rows.append(keyboard_row)
        
        return aiogram.types.ReplyKeyboardMarkup(keyboard=keyboard_rows, resize_keyboard=self.resize_keyboard, one_time_keyboard=self.one_time_keyboard)

class AiogramKeyboardFactory(KeyboardFactory):
    def create_inline_keyboard(self) -> AiogramInlineKeyboard:
        return AiogramInlineKeyboard()
    
    def create_reply_keyboard(self, resize_keyboard: bool = True, one_time_keyboard: bool = False) -> AiogramReplyKeyboard:
        return AiogramReplyKeyboard(resize_keyboard, one_time_keyboard)
