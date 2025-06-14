from api.bot.command.text import TextHandler
from api.bot.keyboard import CallbackHandler
from api.bot.types.payment import PaymentRequest, PaymentItem
from api.placeholder import Placeholder
from shop import ShopRepository
from configs import Messages
from decimal import Decimal

class ShopTextHandler(TextHandler):
    def __init__(self, messages: Messages, shop: ShopRepository):
        self.messages = messages
        self.shop = shop
    
    async def handle(self, message, bot):
        plugins = self.shop.list_plugins()
        if len(plugins) == 0:
            await bot.send_message(message.sender_id, self.messages.shop.empty, parse_mode='HTML')
            return
        
        keyboard = bot.keyboard_factory().create_inline_keyboard()
        for plugin in plugins:
            keyboard.add_button(Placeholder(self.messages.shop.button).place('{name}', plugin.name).build(), f'plugin_{plugin.name}')

        await bot.send_message(message.sender_id, self.messages.shop.message, parse_mode='HTML', keyboard=keyboard)
    
    def pattern(self):
        return self.messages.keyboard.shop

class ShopCallbackHandler(CallbackHandler):
    def __init__(self, messages: Messages, shop: ShopRepository):
        self.messages = messages
        self.shop = shop

    async def handle(self, callback, bot):
        plugin = self.shop.get_plugin(callback.data[7:])
        text = Placeholder('\n'.join(self.messages.shop.entry)) \
            .place('{name}', plugin.name) \
            .place('{description}', plugin.description) \
            .build()

        keyboard = bot.keyboard_factory().create_inline_keyboard()
        keyboard.add_button(self.messages.shop.buy_button, f'buy_{plugin.name}')
        await bot.edit_message(callback.from_user_id, callback.message_id, text, parse_mode='HTML', keyboard=keyboard)
    
    def pattern(self):
        return 'plugin_*'

class BuyCallbackHandler(CallbackHandler):
    def __init__(self, messages: Messages, shop: ShopRepository):
        self.messages = messages
        self.shop = shop

    async def handle(self, callback, bot):
        plugin_name = callback.data[4:]
        plugin = self.shop.get_plugin(plugin_name)
        
        if not plugin:
            await bot.answer_callback(self.messages.shop.not_found)
            return
        
        payment_manager = bot.payment_manager()
        payment_request = PaymentRequest(
            items=[PaymentItem(
                id=plugin.name,
                name=plugin.name,
                price=Decimal('5.00')
            )],
            user_id=callback.from_user_id,
            order_id=f'plugin_{plugin.name}'
        )
        
        payment_response = await payment_manager.create_payment(payment_request)
        
        keyboard = bot.keyboard_factory().create_inline_keyboard()
        keyboard.add_button(self.messages.shop.pay_button, url=payment_response.payment_url)

        text = Placeholder('\n'.join(self.messages.shop.payment_info)) \
            .place('{name}', plugin.name) \
            .place('{price}', payment_response.amount) \
            .build()
        await bot.edit_message(callback.from_user_id, callback.message_id, text, parse_mode='HTML', keyboard=keyboard)
    
    def pattern(self):
        return 'buy_*'
