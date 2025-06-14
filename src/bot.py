from api.aiogram import AiogramBot
from api.configs import ConfigurationManager
from commands import StartCommand
import configs

class PluginsDevBot(AiogramBot):
    def __init__(self, token):
        super().__init__(token)
        manager = ConfigurationManager('configs')

        self.messages = manager.load(configs.Messages, 'messages.yml')

    async def start(self):
        await self.register_command(StartCommand(self.messages))

        return await super().start()
