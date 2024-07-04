from aiogram import types
from aiogram.dispatcher import FSMContext
from apps.telegram.buttons.buttons import subscription_kb, get_tariff_kb, get_subscription_options_kb
from asgiref.sync import sync_to_async
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def start_command(message: types.Message, state: FSMContext):
    welcome_text = (
        "Добро пожаловать в Download Bot!\n\n"
        "Бот предназначен для монтажеров, графических дизайнеров, моушн дизайнеров, фотографам "
        "а также программистам, которые создают сайты.\n\n"
        "Download Bot поможет вам скачивать материалы из сайта Envato Elements.\n\n"
        "Мы дарим вам 1 пробную загрузку, чтобы вы могли проверить наш сервис\n\n"
        "(ссылка) Envato Elements"
    )
    await message.answer(welcome_text, reply_markup=subscription_kb)

async def handle_tariffs(callback_query: types.CallbackQuery):
    tariffs_text = (
        "ПОДПИСКИ:\n"
        "• Месяц: 500 сом. (до 30 скачиваний в день)\n"
        "• Месяц VIP: 1000 сом. (до 100 скачиваний в день)\n\n"
        "ПАКЕТЫ:\n"
        "• 10 скачиваний: 100 сом."
    )
    print("Handling tariffs callback")  # Отладочное сообщение
    kb = await get_tariff_kb()
    await callback_query.message.edit_text(tariffs_text, reply_markup=kb)
    await callback_query.answer()  # Необходимо, чтобы закрыть "thinking" состояние кнопки

async def handle_bonuses(callback_query: types.CallbackQuery):
    bonuses_text = "Бонусы за подписку..."
    print("Handling bonuses callback")  # Отладочное сообщение
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Назад", callback_data='back'))
    await callback_query.message.edit_text(bonuses_text, reply_markup=kb)
    await callback_query.answer()

async def handle_current_subscription(callback_query: types.CallbackQuery):
    current_subscription_text = "Текущая подписка..."
    print("Handling current subscription callback")  # Отладочное сообщение
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Назад", callback_data='back'))
    await callback_query.message.edit_text(current_subscription_text, reply_markup=kb)
    await callback_query.answer()

async def handle_support(callback_query: types.CallbackQuery):
    support_text = "Поддержка..."
    print("Handling support callback")  # Отладочное сообщение
    kb = InlineKeyboardMarkup().row(InlineKeyboardButton("Назад", callback_data='back'))
    await callback_query.message.edit_text(support_text, reply_markup=kb)
    await callback_query.answer()

async def handle_back(callback_query: types.CallbackQuery):
    print("Handling back callback")  # Отладочное сообщение
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

def register_handlers(dp):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_callback_query_handler(handle_tariffs, text='tariffs')
    dp.register_callback_query_handler(handle_bonuses, text='bonuses')
    dp.register_callback_query_handler(handle_current_subscription, text='current_subscription')
    dp.register_callback_query_handler(handle_support, text='support')
    dp.register_callback_query_handler(handle_back, text='back')
    dp.register_callback_query_handler(handle_subscribe_month, text='subscribe_month')
    dp.register_callback_query_handler(handle_subscribe_vip, text='subscribe_vip')
    dp.register_callback_query_handler(handle_subscribe_package, text='subscribe_package')
