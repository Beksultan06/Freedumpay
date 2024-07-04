from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apps.telegram.models import Subscription
from asgiref.sync import sync_to_async

# Кнопки основного меню
subscription_kb = InlineKeyboardMarkup()
subscription_kb.row(
    InlineKeyboardButton("Тарифы", callback_data='tariffs'),
    InlineKeyboardButton("Бонусы за подписку", callback_data='bonuses')
)
subscription_kb.row(
    InlineKeyboardButton("Текущая подписка", callback_data='current_subscription'),
)
subscription_kb.row(
    InlineKeyboardButton("Поддержка", callback_data='support')
)

# Кнопки для выбора тарифов
async def get_tariff_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    subscriptions = await sync_to_async(list)(Subscription.objects.all())
    for subscription in subscriptions:
        kb.add(InlineKeyboardButton(subscription.name, callback_data=f'subscribe_{subscription.id}'))
    kb.row(
        InlineKeyboardButton("Подписка на месяц", callback_data='subscribe_month'),
        InlineKeyboardButton("Подписка на VIP", callback_data='subscribe_vip')
    )
    kb.row(
        InlineKeyboardButton("Пакет", callback_data='subscribe_package')
    )
    kb.row(
        InlineKeyboardButton("Назад", callback_data='back')
    )
    return kb

# Кнопки для подписки
def get_subscription_options_kb():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.row(
        InlineKeyboardButton("Подписка на месяц", callback_data='subscribe_month'),
    )
    kb.row(
        InlineKeyboardButton("Подписка на VIP", callback_data='subscribe_vip')
    )
    kb.row(
        InlineKeyboardButton("Пакет", callback_data='subscribe_package')
    )
    kb.row(
        InlineKeyboardButton("Назад", callback_data='back')
    )
    return kb
