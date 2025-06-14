from api.aiogram import AiogramBot
from api.configs import ConfigurationManager
from api.bot.keyboard import Keyboard, Button
from api.bot.payment.provider import PaymentManager, PaymentProvider
from api.bot.types.payment import PaymentNotification
from commands import StartCommand, AdminCommand
from shop import DatabaseShopRepository, ShopPaymentHandler
from callbacks import ShopTextHandler, ShopCallbackHandler, BuyCallbackHandler, AdminPasswordTextHandler, AdminBackTextHandler
from keyboard import KeyboardManager
from fastapi import FastAPI, Form, Request
from decimal import Decimal
import asyncio
import uvicorn
import configs

class PluginsDevBot(AiogramBot):
    def __init__(self, token: str, payment_provider: PaymentProvider, admin_password: str, webhook_host: str = '0.0.0.0', webhook_port: int = 8050):
        payment_manager = PaymentManager(payment_provider)
        super().__init__(token, payment_manager)
        
        self.admin_password = admin_password
        
        self.webhook_host = webhook_host
        self.webhook_port = webhook_port
        self.app = FastAPI(title='PluginsDevBot Webhook')
        
        manager = ConfigurationManager('configs')
        self.config = manager.load(configs.Config, 'config.yml')
        self.messages = manager.load(configs.Messages, 'messages.yml')

        self.keyboard_manager = KeyboardManager(self.keyboardfactory, self.messages)

        db_config = self.config.database
        self.shop = DatabaseShopRepository(
            db_type=db_config.type,
            db_name=db_config.path,
            host=db_config.host,
            port=db_config.port,
            user=db_config.user, 
            password=db_config.password
        )
        
        shop_payment_handler = ShopPaymentHandler(self.messages, self.shop, self)
        payment_manager.add_handler(shop_payment_handler)
        
        self._setup_webhook_routes()

    def _setup_webhook_routes(self):
        @self.app.post('/yoomoney/webhook')
        async def yoomoney_webhook(
            request: Request,
            notification_type: str = Form(),
            operation_id: str = Form(),
            amount: str = Form(),
            currency: str = Form(),
            datetime: str = Form(),
            sender: str = Form(),
            codepro: str = Form(),
            label: str = Form(),
            sha1_hash: str = Form(),
            unaccepted: str = Form(default='false'),
            test_notification: str = Form(default='false')
        ):
            try:
                notification = PaymentNotification(
                    operation_id=operation_id,
                    amount=Decimal(amount),
                    currency=currency,
                    datetime=datetime,
                    sender=sender,
                    label=label,
                    notification_type=notification_type,
                    codepro=codepro.lower() == 'true',
                    sha1_hash=sha1_hash,
                    unaccepted=unaccepted.lower() == 'true',
                    test_notification=test_notification.lower() == 'true'
                )
                
                payment_manager = self.payment_manager()
                await payment_manager.process_notification(notification)
            except Exception as exception:
                return {'error': str(exception)}
            
            return 'OK'
    
    async def start(self):
        await self.register_command(StartCommand(self.messages, self.keyboard_manager))
        await self.register_command(AdminCommand(self.messages))

        await self.register_text_handler(ShopTextHandler(self.messages, self.shop))
        await self.register_text_handler(AdminPasswordTextHandler(self.messages, self.keyboard_manager, self.admin_password))
        await self.register_text_handler(AdminBackTextHandler(self.messages, self.keyboard_manager))

        await self.register_callback_handler(ShopCallbackHandler(self.messages, self.shop))
        await self.register_callback_handler(BuyCallbackHandler(self.messages, self.shop))
        
        webhook_task = asyncio.create_task(self._start_webhook_server())
        bot_task = asyncio.create_task(super().start())
        
        await asyncio.gather(webhook_task, bot_task)

    async def _start_webhook_server(self):
        config = uvicorn.Config(
            app=self.app,
            host=self.webhook_host,
            port=self.webhook_port,
            log_level='info'
        )
        await uvicorn.Server(config).serve()
