from django.core.management.base import BaseCommand
from aiogram.utils import executor
from apps.telegram.management.commands.bot import dp
from apps.telegram.management.commands.main import register_handlers

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **kwargs):
        register_handlers(dp)
        executor.start_polling(dp, skip_updates=True)
