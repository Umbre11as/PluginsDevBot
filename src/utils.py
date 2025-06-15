from api.placeholder import Placeholder
import os

class PluginSender:
    @staticmethod
    async def send_plugin(bot, user_id, plugin, messages):
        if os.path.exists(plugin.file_path):
            caption = Placeholder(messages.shop.caption).place('{name}', plugin.name).build()
            await bot.send_document(user_id, str(plugin.file_path), caption=caption)
        else:
            await bot.send_message(
                user_id, 
                Placeholder('\n'.join(messages.shop.file_not_found)).place('{operation_id}', 'manual').build(), 
                parse_mode='HTML'
            )
