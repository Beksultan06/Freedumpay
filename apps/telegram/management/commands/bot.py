import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import os
import django

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from core.settings import API_TOKEN
from apps.telegram.management.commands.main import register_handlers

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Регистрация обработчиков
register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
