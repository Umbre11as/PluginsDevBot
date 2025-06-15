from api.placeholder import Placeholder
from api.bot.types import Message, CallbackQuery
from keyboard import KeyboardManager
from shop import ShopRepository
from configs import Messages
from admin.wait import WaitStates
from admin.base import AdminTextHandler, AdminCallbackHandler
from utils import PluginSender
from decimal import Decimal

class AdminShopStateHandler(AdminTextHandler):
    def __init__(self, messages: Messages, shop: ShopRepository):
        super().__init__(messages)
        self.shop = shop

    async def handle_admin(self, message: Message, bot):
        user_id = message.sender_id
        state = WaitStates.get_state(user_id)
        
        if not state or not state['state'].startswith('admin_shop_'):
            return
        
        await self._handle_state(message, bot, state)

    async def _handle_state(self, message: Message, bot, state):
        user_id = message.sender_id
        current_state = state['state']
        
        if current_state == 'admin_shop_title':
            state['data']['title'] = message.text
            WaitStates.set_state(user_id, 'admin_shop_description', state['data'])
            await bot.send_message(user_id, self.messages.admin.shop.enter.description, parse_mode='HTML')
        elif current_state == 'admin_shop_description':
            data = state.get('data', {})
            data['description'] = message.text
            WaitStates.set_state(user_id, 'admin_shop_price', data)
            await bot.send_message(user_id, self.messages.admin.shop.enter.price, parse_mode='HTML')
        elif current_state == 'admin_shop_price':
            try:
                price = Decimal(message.text)
                state['data']['price'] = price
                WaitStates.set_state(user_id, 'admin_shop_file', state['data'])
            except:
                await bot.send_message(user_id, self.messages.admin.shop.enter.price, parse_mode='HTML')
        elif current_state == 'admin_shop_give_user':
            plugin_name = state['data']['plugin_name']
            plugin = self.shop.get_plugin(plugin_name)
            
            if not plugin:
                await bot.send_message(user_id, self.messages.shop.not_found, parse_mode='HTML')
                WaitStates.clear_state(user_id)
                return
            
            try:
                if message.text.startswith('@'):
                    await bot.send_message(user_id, self.messages.admin.shop.enter.not_username, parse_mode='HTML')
                    return
                else:
                    target_user_id = int(message.text)
                
                await PluginSender.send_plugin(bot, target_user_id, plugin, self.messages)
                await bot.send_message(user_id, self.messages.admin.shop.give.success, parse_mode='HTML')
            except Exception as exception:
                text = Placeholder(self.messages.admin.shop.give.fail).place('{exception}', str(exception)).build()
                await bot.send_message(user_id, text, parse_mode='HTML')
            
            WaitStates.clear_state(user_id)

    def pattern(self):
        return '*'

class AdminShopFileHandler(AdminTextHandler):
    def __init__(self, messages: Messages, shop: ShopRepository):
        super().__init__(messages)
        self.shop = shop
    
    async def handle_admin(self, message: Message, bot):
        user_id = message.sender_id
        state = WaitStates.get_state(user_id)
        
        if not state or state['state'] != 'admin_shop_file':
            return
        
        if not message.document:
            await bot.send_message(user_id, self.messages.admin.shop.enter.send, parse_mode='HTML')
            return
        
        try:
            file_path = f'plugins/{state['data']['title']}.jar'
            await bot.download_file(message.document.file_id, file_path)
            
            self.shop.add_plugin(
                name=state['data']['title'],
                description=state['data']['description'],
                file_path=file_path,
                price=state['data']['price']
            )
            
            await bot.send_message(user_id, self.messages.admin.shop.copy.success, parse_mode='HTML')
        except Exception as exception:
            text = Placeholder(self.messages.admin.shop.copy.fail).place('{exception}', str(exception)).build()
            await bot.send_message(user_id, text, parse_mode='HTML')
        
        WaitStates.clear_state(user_id)
    
    def pattern(self):
        return '*'

class AdminAddPluginCallbackHandler(AdminCallbackHandler):
    def __init__(self, messages: Messages):
        super().__init__(messages)
    
    async def handle_admin(self, callback: CallbackQuery, bot):
        user_id = callback.from_user_id
        WaitStates.set_state(user_id, 'admin_shop_title', {})
        await bot.edit_message(user_id, callback.message_id, self.messages.admin.shop.enter.title, parse_mode='HTML')
    
    def pattern(self):
        return 'admin_add_plugin'

class AdminPluginCallbackHandler(AdminCallbackHandler):
    def __init__(self, messages: Messages, shop: ShopRepository):
        super().__init__(messages)
        self.shop = shop
    
    async def handle_admin(self, callback: CallbackQuery, bot):
        plugin_name = callback.data[13:]
        plugin = self.shop.get_plugin(plugin_name)
        
        if not plugin:
            await bot.answer_callback(callback.id, self.messages.shop.not_found)
            return
        
        text = Placeholder('\n'.join(self.messages.shop.entry)) \
            .place('{name}', plugin.name) \
            .place('{description}', plugin.description) \
            .place('{price}', str(plugin.price)) \
            .build()
        
        keyboard = bot.keyboard_factory().create_inline_keyboard()
        keyboard.add_button(self.messages.admin.shop.plugin.delete, f'admin_delete_{plugin.name}')
        keyboard.add_button(self.messages.admin.shop.plugin.give, f'admin_give_{plugin.name}')
        
        await bot.edit_message(callback.from_user_id, callback.message_id, text, parse_mode='HTML', keyboard=keyboard)
    
    def pattern(self):
        return 'admin_plugin_*'

class AdminDeletePluginCallbackHandler(AdminCallbackHandler):
    def __init__(self, messages: Messages, shop: ShopRepository):
        super().__init__(messages)
        self.shop = shop
    
    async def handle_admin(self, callback: CallbackQuery, bot):
        plugin_name = callback.data[13:]
        self.shop.remove_plugin(plugin_name)
        
        await bot.answer_callback(callback.id, self.messages.admin.shop.removed)
        
        plugins = self.shop.list_plugins()
        keyboard = bot.keyboard_factory().create_inline_keyboard()
        
        keyboard.add_button(self.messages.admin.shop.add, 'admin_add_plugin')
        keyboard.add_row()
        
        for i in range(0, len(plugins), 2):
            for j in range(i, min(i + 2, len(plugins))):
                plugin = plugins[j]
                text = Placeholder(self.messages.admin.shop.button).place('{name}', plugin.name).build()
                keyboard.add_button(text, f'admin_plugin_{plugin.name}')
            if i + 2 < len(plugins):
                keyboard.add_row()
        
        await bot.edit_message(callback.from_user_id, callback.message_id, self.messages.admin.shop.welcome, parse_mode='HTML', keyboard=keyboard)
    
    def pattern(self):
        return 'admin_delete_*'

class AdminGivePluginCallbackHandler(AdminCallbackHandler):
    def __init__(self, messages: Messages):
        super().__init__(messages)
    
    async def handle_admin(self, callback: CallbackQuery, bot):
        plugin_name = callback.data[11:]
        user_id = callback.from_user_id
        
        WaitStates.set_state(user_id, 'admin_shop_give_user', {'plugin_name': plugin_name})
        await bot.edit_message(user_id, callback.message_id, self.messages.admin.shop.enter.user, parse_mode='HTML')
    
    def pattern(self):
        return 'admin_give_*'

class AdminShopMenuHandler(AdminTextHandler):
    def __init__(self, messages: Messages, shop: ShopRepository, keyboard_manager: KeyboardManager):
        super().__init__(messages)
        self.shop = shop
        self.keyboard_manager = keyboard_manager

    async def handle_admin(self, message, bot):
        plugins = self.shop.list_plugins()
        keyboard = bot.keyboard_factory().create_inline_keyboard()
        
        keyboard.add_button(self.messages.admin.shop.add, 'admin_add_plugin')
        keyboard.add_row()
        
        for i in range(0, len(plugins), 2):
            for j in range(i, min(i + 2, len(plugins))):
                plugin = plugins[j]
                text = Placeholder(self.messages.admin.shop.button).place('{name}', plugin.name).build()
                keyboard.add_button(text, f'admin_plugin_{plugin.name}')
            if i + 2 < len(plugins):
                keyboard.add_row()

        await bot.send_message(message.sender_id, self.messages.admin.shop.welcome, parse_mode='HTML', keyboard=keyboard)

    def pattern(self):
        return self.messages.admin.keyboard.shop
