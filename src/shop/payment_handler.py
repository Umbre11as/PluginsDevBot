from api.bot.payment.provider import PaymentHandler
from api.bot.types.payment import PaymentNotification
from api.placeholder import Placeholder
from .database.repository import ShopRepository
from configs import Messages
from utils import PluginSender

class ShopPaymentHandler(PaymentHandler):
    def __init__(self, messages: Messages, shop: ShopRepository, bot):
        self.messages = messages
        self.shop = shop
        self.bot = bot
    
    async def on_payment_success(self, notification: PaymentNotification, user_id: int, order_id: str):
        if order_id.startswith('plugin_'):
            plugin_name = order_id[7:]
            plugin = self.shop.get_plugin(plugin_name)
            
            if not plugin:
                await self.bot.send_message(
                    user_id,
                    Placeholder('\n'.join(self.messages.shop.plugin_not_found_after_payment)).place('{operation_id}', notification.operation_id).build(),
                    parse_mode='HTML'
                )
                return

            await self.bot.send_message(
                user_id,
                Placeholder('\n'.join(self.messages.shop.success_payment)).place('{name}', plugin.name).build(),
                parse_mode='HTML'
            )
            
            await PluginSender.send_plugin(self.bot, user_id, plugin, self.messages)
    
    async def on_payment_failed(self, notification: PaymentNotification, user_id: int, order_id: str):
        await self.bot.send_message(user_id, Placeholder('\n'.join(self.messages.shop.payment_failed)).place('{operation_id}', notification.operation_id).build(), parse_mode='HTML')
