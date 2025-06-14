from ...bot import Bot
from ...bot.keyboard_factory import KeyboardFactory
from ...bot.keyboard import CallbackHandler, Keyboard
from ...bot.command.text import TextHandler
from ...bot.payment.provider import PaymentManager
from ..bot.keyboard import AiogramKeyboardFactory, AiogramCallbackManager
from ..bot.command import AiogramCommandHandler, Command
from ..bot.command import AiogramTextManager
from typing import Optional
import aiogram

class AiogramBot(Bot):
    def __init__(self, token: str, payment_manager: Optional[PaymentManager] = None):
        self.telegram = aiogram.Bot(token)
        self.dispatcher = aiogram.Dispatcher()
        self.command_handler = AiogramCommandHandler(self, self.dispatcher)
        self.keyboardfactory = AiogramKeyboardFactory()
        self.callback_manager = AiogramCallbackManager(self, self.dispatcher)
        self.text_manager = AiogramTextManager(self, self.dispatcher)
        self.paymentmanager = payment_manager

    async def register_command(self, command: Command):
        self.command_handler.register(command)

    async def send_message(self, id: int, text: str, keyboard: Optional[Keyboard] = None, parse_mode='MarkdownV2'):
        reply_markup = None
        if keyboard:
            reply_markup = keyboard.build()
        
        await self.telegram.send_message(id, text, parse_mode=parse_mode, reply_markup=reply_markup)

    async def edit_message(self, user_id: int, message_id: int, text: str, keyboard: Optional[Keyboard] = None, parse_mode='MarkdownV2'):
        reply_markup = None
        if keyboard:
            reply_markup = keyboard.build()
        
        await self.telegram.edit_message_text(
            text=text, 
            chat_id=user_id, 
            message_id=message_id, 
            parse_mode=parse_mode, 
            reply_markup=reply_markup
        )
    
    async def answer_callback(self, callback_id: str, text: str = '', show_alert: bool = False):
        await self.telegram.answer_callback_query(callback_id, text, show_alert)
    
    def keyboard_factory(self) -> KeyboardFactory:
        return self.keyboardfactory

    async def register_callback_handler(self, handler: CallbackHandler):
        self.callback_manager.register(handler)
    
    async def register_text_handler(self, handler: TextHandler):
        self.text_manager.register(handler)
    
    def payment_manager(self) -> PaymentManager:
        return self.paymentmanager
    
    async def start(self):
        await super().start()

        self.callback_manager.setup_handlers()
        self.text_manager.setup_handlers()
        await self.dispatcher.start_polling(self.telegram)
