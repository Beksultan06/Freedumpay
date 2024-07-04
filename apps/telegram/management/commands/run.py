from django.core.management.base import BaseCommand
from apps.telegram.management.commands.bot import dp

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **kwargs):
        from aiogram.utils import executor
        executor.start_polling(dp, skip_updates=True)
    