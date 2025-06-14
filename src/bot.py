from api.aiogram import AiogramBot
from api.configs import ConfigurationManager
from commands import StartCommand
from shop import DatabaseShopRepository
import configs

class PluginsDevBot(AiogramBot):
    def __init__(self, token):
        super().__init__(token)
        manager = ConfigurationManager('configs')

        self.config = manager.load(configs.Config, 'config.yml')
        self.messages = manager.load(configs.Messages, 'messages.yml')

        db_config = self.config.database
        self.shop = DatabaseShopRepository(
            db_type=db_config.type,
            db_name=db_config.path,
            host=db_config.host,
            port=db_config.port,
            user=db_config.user, 
            password=db_config.password
        )

    async def start(self):
        await self.register_command(StartCommand(self.messages))

        return await super().start()
