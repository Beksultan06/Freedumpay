import os, requests, logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
from database import add_subscriber, is_subscriber, update_remaining_downloads, get_remaining_downloads

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv('.env')
bot = Bot(os.environ.get('token'))
dp = Dispatcher(bot)

DB_FILE = 'subscribers.db'
tariff_link = "https://elements.envato.com/ru/grunge-logo-intro-X2CJB45"

async def start(message: types.Message):
    chat_id = message.chat.id
    if not is_subscriber(chat_id):
        add_subscriber(chat_id)
        bonus_button = InlineKeyboardButton("Бонусы", callback_data="bonus")
        tariff_button = InlineKeyboardButton("Тарифы", callback_data="tariff")
        keyboard = InlineKeyboardMarkup().add(bonus_button, tariff_button)
        await bot.send_message(chat_id=chat_id, text="Привет! Вы получаете 3 бесплатных скачивания после нажатия кнопки 'Бонусы' или можете ознакомиться с нашими тарифами.", reply_markup=keyboard)
    else:
        await show_tariffs(chat_id)

async def bonus(message: types.Message):
    chat_id = message.chat.id
    bonus_link = "https://elements.envato.com/ru/grunge-logo-intro-X2CJB45"
    await bot.send_message(chat_id=chat_id, text=f"Вы получаете 3 бесплатных скачивания. Вот ваш бонусный материал: {bonus_link}")

async def handle_text(message: types.Message):
    pass

async def handle_material_link(message: types.Message):
    chat_id = message.chat.id
    material_link = message.text

    remaining_downloads = get_remaining_downloads(chat_id)

    if remaining_downloads > 0:
        update_remaining_downloads(chat_id, remaining_downloads - 1)

        try:
            response = requests.get(material_link)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                if 'text/html' in content_type:
                    await bot.send_message(chat_id=chat_id, text="Это ссылка на веб-страницу. Пожалуйста, отправьте прямую ссылку на файл.")
                else:
                    file_name = material_link.split('/')[-1]
                    with open(file_name, 'wb') as file:
                        file.write(response.content)
                    await bot.send_document(chat_id=chat_id, document=open(file_name, 'rb'))
                    os.remove(file_name)
            else:
                await bot.send_message(chat_id=chat_id, text="Не удалось загрузить материал.")
        except Exception as e:
            logger.error(f"Error handling material link: {e}")
            await bot.send_message(chat_id=chat_id, text="Произошла ошибка при обработке ссылки.")
    else:
        await bot.send_message(chat_id=chat_id, text="У вас закончились бесплатные скачивания.")

async def buy(message: types.Message):
    try:
        chat_id = message.chat.id
        monthly_button = InlineKeyboardButton("Подписка на месяц - 400 сом", callback_data="subscribe_monthly")
        vip_button = InlineKeyboardButton("VIP подписка - 1000 сом", callback_data="subscribe_vip")
        five_downloads_button = InlineKeyboardButton("5 скачиваний - 100 сом", callback_data="download_5")
        fifteen_downloads_button = InlineKeyboardButton("15 скачиваний - 250 сом", callback_data="download_15")
        keyboard = InlineKeyboardMarkup().row(monthly_button, vip_button).row(five_downloads_button, fifteen_downloads_button)
        await bot.send_message(chat_id=chat_id, text="Выберите тариф:", reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Ошибка в обработке команды /buy: {e}")

async def help_command(query: types.CallbackQuery):
    await help_command(query.message)

async def handle_button(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    data = query.data
    if data == 'help':
        await help_command(query)
    elif data == 'subscribe_monthly':
        await ask_confirmation(chat_id, 'subscribe_monthly', query.message.message_id)
    elif data == 'subscribe_vip':
        await ask_confirmation(chat_id, 'subscribe_vip', query.message.message_id)
    elif data == 'download_5':
        await ask_confirmation(chat_id, 'download_5', query.message.message_id)
    elif data == 'download_15':
        await ask_confirmation(chat_id, 'download_15', query.message.message_id)
    elif data == 'bonus':
        await bonus(query.message)
    elif data == 'tariff':  
        await show_tariffs(chat_id)
    elif data.startswith('confirm_'):
        await process_confirmation(chat_id, data[len('confirm_'):], query.message.message_id)
    elif data.startswith('cancel_'):
        await cancel_confirmation(chat_id, query.message.message_id)

async def ask_confirmation(chat_id, action, message_id):
    confirmation_keyboard = InlineKeyboardMarkup().row(
        InlineKeyboardButton        ("Да", callback_data=f"confirm_{action}"),
        InlineKeyboardButton("Нет", callback_data=f"cancel_{message_id}")
    )
    await bot.send_message(chat_id=chat_id, text="Вы уверены, что хотите выбрать этот тариф?", reply_markup=confirmation_keyboard)

async def process_confirmation(chat_id, action, message_id):
    if action.startswith('subscribe'):
        await process_subscription_payment(chat_id, action)
    elif action.startswith('download'):
        await process_download_payment(chat_id, action)
    else:
        await bot.send_message(chat_id=chat_id, text="Действие отменено.")

async def process_subscription_payment(chat_id, subscription_type):
    try:
        await bot.send_message(chat_id=chat_id, text=f"Подписка типа '{subscription_type.split('_')[-1]}' успешно активирована! Ссылка на сайт: {tariff_link}")
    except Exception as e:
        await bot.send_message(chat_id=chat_id, text="Произошла ошибка при активации подписки. Пожалуйста, попробуйте еще раз или обратитесь в службу поддержки.")
        logger.error(f"Ошибка в обработке команды /buy: {e}")

async def process_download_payment(chat_id, num_downloads):
    try:
        update_remaining_downloads(chat_id, get_remaining_downloads(chat_id) + int(num_downloads.split('_')[-1]))
        await bot.send_message(chat_id=chat_id, text=f"Куплено {num_downloads.split('_')[-1]} скачиваний! Ссылка на сайт: {tariff_link}")
    except Exception as e:
        await bot.send_message(chat_id=chat_id, text="Произошла ошибка при покупке скачиваний. Пожалуйста, попробуйте еще раз или обратитесь в службу поддержки.")
        logger.error(f"Ошибка при покупке скачиваний: {e}")

async def show_tariffs(chat_id):
    tariffs_message = "Доступные тарифы:\n\n" \
                      "1. Подписка на месяц - 400 сом (до 30 скачиваний в день)\n" \
                      "2. VIP подписка - 1000 сом (до 100 скачиваний в день)\n" \
                      "3. 15 скачиваний - 250 сом (Будет активно пока не закончится количество скачиваний)\n" \
                      "4. 5 скачиваний - 100 сом (Будет активно пока не закончится количество скачиваний)\n" \
                      "чтобы приобрести тарифы нажмите на кнопку /buy\n\n" 
    await bot.send_message(chat_id=chat_id, text=tariffs_message)

async def cancel_confirmation(chat_id, message_id):
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Выберите тариф:", reply_markup=create_tariff_keyboard())

def create_tariff_keyboard():
    monthly_button = InlineKeyboardButton("Подписка на месяц - 400 сом", callback_data="subscribe_monthly")
    vip_button = InlineKeyboardButton("VIP подписка - 1000 сом", callback_data="subscribe_vip")
    five_downloads_button = InlineKeyboardButton("5 скачиваний - 100 сом", callback_data="download_5")
    fifteen_downloads_button = InlineKeyboardButton("15 скачиваний - 250 сом", callback_data="download_15")
    return InlineKeyboardMarkup().row(monthly_button, vip_button).row(five_downloads_button, fifteen_downloads_button)

async def error_handler(update, exception):
    logger.error(f"Update {update} caused error: {exception}")



