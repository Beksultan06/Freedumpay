from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

bonus_button = InlineKeyboardButton("Бонусы", callback_data="bonus")
tariff_button = InlineKeyboardButton("Тарифы", callback_data="tariff")
tarif = InlineKeyboardMarkup().add(bonus_button, tariff_button)

monthly_button = InlineKeyboardButton("Подписка на месяц - 400 сом", callback_data="subscribe_monthly")
vip_button = InlineKeyboardButton("VIP подписка - 1000 сом", callback_data="subscribe_vip")
five_downloads_button = InlineKeyboardButton("5 скачиваний - 100 сом", callback_data="download_5")
fifteen_downloads_button = InlineKeyboardButton("15 скачиваний - 250 сом", callback_data="download_15")
keyboard = InlineKeyboardMarkup().row(monthly_button, vip_button).row(five_downloads_button, fifteen_downloads_button)

monthly_button1 = InlineKeyboardButton("Подписка на месяц - 400 сом", callback_data="subscribe_monthly")
vip_button = InlineKeyboardButton("VIP подписка - 1000 сом", callback_data="subscribe_vip")
five_downloads_button = InlineKeyboardButton("5 скачиваний - 100 сом", callback_data="download_5")
fifteen_downloads_button = InlineKeyboardButton("15 скачиваний - 250 сом", callback_data="download_15")