import requests
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from asgiref.sync import sync_to_async
from apps.telegram.buttons.buttons import subscription_kb, get_tariff_kb
from apps.telegram.models import UserDownload
from .bot import dp
import logging


logging.basicConfig(level=logging.INFO)

# Начальная команда /start
async def start_command(message: types.Message, state: FSMContext):
    user, created = await sync_to_async(UserDownload.objects.get_or_create)(user_id=message.from_user.id)
    if created or user.download_count == 0:
        welcome_text = (
            "Добро пожаловать в Download Bot!\n\n"
            "Бот предназначен для монтажеров, графических дизайнеров, моушн дизайнеров, фотографам "
            "а также программистам, которые создают сайты.\n\n"
            "Download Bot поможет вам скачивать материалы из сайта Envato Elements.\n\n"
            "Мы дарим вам 1 пробную загрузку, чтобы вы могли проверить наш сервис\n\n"
            "(ссылка) Envato Elements"
        )
        logging.info("Работает")
    else:
        welcome_text = (
            "Добро пожаловать в Download Bot!\n\n"
            "Ваш пробный период истек.\n\n"
            "Вы можете приобрести подписку, чтобы продолжить скачивание.\n\n"
            "Используйте команду /pay для покупки подписки."
        )
        logging.info("Работает")
    await message.answer(welcome_text, reply_markup=subscription_kb)

# Остальные функции
async def handle_tariffs(callback_query: types.CallbackQuery):
    tariffs_text = (
        "ПОДПИСКИ:\n"
        "• Месяц: 799 р. (до 20 скачиваний в день)\n"
        "• 👑Месяц VIP: 1880 р. (до 100 скачиваний в день)\n\n"
        "ПАКЕТЫ:\n"
        "• 20 скачиваний: 599 р."
    )
    kb = await get_tariff_kb()
    await callback_query.message.edit_text(tariffs_text, reply_markup=kb)
    await callback_query.answer()

async def handle_bonuses(callback_query: types.CallbackQuery):
    bonuses_text = "Вы уже получили бесплатное скачивание за подписку на группу!"
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Назад", callback_data='back'))
    await callback_query.message.edit_text(bonuses_text, reply_markup=kb)
    await callback_query.answer()

async def handle_current_subscription(callback_query: types.CallbackQuery):
    current_subscription_text = """Вы можете скачать 1 файлов

Чтобы скачивать больше - вы можете приобрести нашу подписку.
Больше информации в команде /pay

Чтобы отвязать карту и завершить подписку: /sub_end"""
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Назад", callback_data='back'))
    await callback_query.message.edit_text(current_subscription_text, reply_markup=kb)
    await callback_query.answer()

async def handle_pay(message: types.Message):
    tariffs_text = (
        "У вас закончились скачивания/подписка 😢\n"
        "Но вы можете приобрести её\n\n"
        "ПОДПИСКИ:\n"
        "• Месяц: 799 р. (до 20 скачиваний в день)\n"
        "• 👑Месяц VIP: 1880 р. (до 100 скачиваний в день)\n\n"
        "ПАКЕТЫ:\n"
        "• 20 скачиваний: 599 р."
    )
    kb = await get_tariff_kb()
    await message.answer(tariffs_text, reply_markup=kb)

async def handle_support(callback_query_or_message: types.CallbackQuery | types.Message):
    support_text = "Текущий агент поддержки на связи: @admin"
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Назад", callback_data='back'))
    
    if isinstance(callback_query_or_message, types.CallbackQuery):
        await callback_query_or_message.message.edit_text(support_text, reply_markup=kb)
        await callback_query_or_message.answer()
    else:
        await callback_query_or_message.answer(support_text, reply_markup=kb)

async def handle_back(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text("Добро пожаловать в Download Bot!\n\n"
                                           "Бот предназначен для монтажеров, графических дизайнеров, моушн дизайнеров, фотографам "
                                           "а также программистам, которые создают сайты.\n\n"
                                           "Download Bot поможет вам скачивать материалы из сайта Envato Elements.\n\n"
                                           "Мы дарим вам 1 пробную загрузку, чтобы вы могли проверить наш сервис\n\n"
                                           "(ссылка) Envato Elements", reply_markup=subscription_kb)
    await callback_query.answer()

async def handle_subscribe_month(callback_query: types.CallbackQuery):
    text = (
        """Оплата промо подписки на квартал
на SP Download Bot за 500 сом.

Ссылка (на оплату): """
    )
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Назад", callback_data='tariffs'))
    kb.row(InlineKeyboardButton("Перейти к оплате", url="https://example.com/pay_month"))
    await callback_query.message.edit_text(text, reply_markup=kb)
    await callback_query.answer()

async def handle_subscribe_vip(callback_query: types.CallbackQuery):
    text = (
        """Оплата промо подписки на квартал
на SP Download Bot за 1000 сом.

Ссылка (на оплату): """
    )
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Назад", callback_data='tariffs'))
    kb.row(InlineKeyboardButton("Перейти к оплате", url="https://example.com/pay_vip"))
    await callback_query.message.edit_text(text, reply_markup=kb)
    await callback_query.answer()

async def handle_subscribe_package(callback_query: types.CallbackQuery):
    text = (
       """Оплата промо подписки на квартал
на SP Download Bot за 100 сом.

Ссылка (на оплату): """
    )
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Назад", callback_data='tariffs'))
    kb.row(InlineKeyboardButton("Перейти к оплате", url="https://example.com/pay_package"))
    await callback_query.message.edit_text(text, reply_markup=kb)
    await callback_query.answer()

async def handle_sub_end(message: types.Message):
    await message.answer("Ваша подписка была отменена!")

# Регистрация обработчиков
def register_handlers(dp):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(handle_pay, commands=['pay'])
    dp.register_message_handler(handle_sub_end, commands=['sub_end'])
    dp.register_message_handler(handle_support, commands=['support'])  # Добавляем команду /support
    dp.register_callback_query_handler(handle_tariffs, text='tariffs')
    dp.register_callback_query_handler(handle_bonuses, text='bonuses')
    dp.register_callback_query_handler(handle_current_subscription, text='current_subscription')
    dp.register_callback_query_handler(handle_support, text='support')  # Добавляем обработчик кнопки 'support'
    dp.register_callback_query_handler(handle_back, text='back')
    dp.register_callback_query_handler(handle_subscribe_month, text='subscribe_month')
    dp.register_callback_query_handler(handle_subscribe_vip, text='subscribe_vip')
    dp.register_callback_query_handler(handle_subscribe_package, text='subscribe_package')
