import asyncio
from main import dp
from main import buy, error_handler, handle_button, handle_material_link, handle_text, help_command, start
from aiogram import types

async def main():
    # Регистрируем обработчики
    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(buy, commands="buy")
    dp.register_message_handler(help_command, commands="help")
    dp.register_message_handler(handle_text, content_types=types.ContentType.TEXT)
    dp.register_message_handler(handle_material_link, content_types=types.ContentType.TEXT, regexp=r'https?://\S+')
    dp.register_callback_query_handler(handle_button, lambda query: query.data in ['help', 'subscribe_monthly', 'subscribe_vip', 'download_5', 'download_15', 'bonus', 'tariff'])
    dp.register_callback_query_handler(handle_button, lambda query: query.data.startswith('confirm_') or query.data.startswith('cancel_'))

    # Регистрируем обработчик ошибок
    dp.errors_handler(error_handler)
    
    # Запускаем бота
    await dp.start_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())