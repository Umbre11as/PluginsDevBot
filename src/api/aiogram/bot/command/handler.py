from ....bot.command import CommandHandler, Message, Command
from ..util import Adapter
import aiogram
import aiogram.filters

class AiogramCommandHandler(CommandHandler):
    def __init__(self, bot, dispatcher: aiogram.Dispatcher):
        super().__init__(bot)
        self.dispatcher = dispatcher
    
    def register(self, command: Command):
        for alias in command.aliases():
            @self.dispatcher.message(aiogram.filters.Command(alias))
            async def handler(message: aiogram.types.Message):
                await command.handle(Adapter.to_message(message), self.bot)
