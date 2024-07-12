import logging
import requests
from aiogram import Bot, Dispatcher, executor, types
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle

# Вставьте сюда ваш токен Telegram-бота
TOKEN = '6573964275:AAFQYZ_JqNA9ND4hGhYNX4fvutv1D-sE-RA'
ENVATO_EMAIL = 'timtima704@gmail.com'
ENVATO_PASSWORD = 'Tim_TIM9524'

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем объект бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Сессия для авторизации
session = requests.Session()

def login_to_envato():
    # Настройка Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Открываем страницу логина
        login_page_url = "https://account.envato.com/sign_in"
        driver.get(login_page_url)

        # Ждем загрузки страницы
        time.sleep(5)

        # Вводим email
        email_input = driver.find_element(By.NAME, "username")
        email_input.send_keys(ENVATO_EMAIL)
        
        # Ждем перед вводом пароля
        time.sleep(2)

        # Вводим пароль
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(ENVATO_PASSWORD)
        password_input.send_keys(Keys.RETURN)

        # Ждем загрузки страницы после входа
        time.sleep(10)

        # Проверка успешного входа
        if "dashboard" in driver.current_url:
            logging.info("Successfully logged in to Envato")

            # Сохраняем куки в файл
            with open('envato_cookies.pkl', 'wb') as file:
                pickle.dump(driver.get_cookies(), file)
        else:
            logging.error("Failed to log in to Envato")
            raise Exception("Login failed")
    finally:
        driver.quit()

def load_cookies(session, filepath):
    with open(filepath, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправьте мне ссылку на Envato Elements, и я скачаю файл для вас.")

@dp.message_handler(commands=['register'])
async def handle_register(message: types.Message):
    await message.reply("Регистрация уже выполнена заранее.")

@dp.message_handler()
async def download_file(message: types.Message):
    url = message.text
    logging.info(f'\n\n\n\nссылка {url}\n\n\n\n')

    if 'envato.com' not in url:
        await message.reply('Пожалуйста, предоставьте действительную ссылку на Envato Elements.')
        return

    try:
        login_to_envato()
        load_cookies(session, 'envato_cookies.pkl')

        # Попробуем получить ссылку для скачивания из страницы
        response = session.get(url)
        logging.info(f'\n\n\n\nссылка {response}\n\n\n\n')
        if response.status_code != 200:
            logging.error(f"Failed to load file page: {response.status_code}, {response.text}")
            await message.reply('Не удалось загрузить страницу файла.')
            return
        print("Успешно 2")
        # Поиск ссылки на скачивание на странице
        download_link = None
        if 'content-length' in response.headers:
            download_link = url
        else:
            content = response.content.decode('utf-8')
            start = content.find('href="') + len('href="')
            end = content.find('"', start)
            if start > len('href="') - 1 and end > start:
                download_link = content[start:end]
        print("Успешно 3")
        if download_link is None:
            logging.error("Download link not found")
            await message.reply('Не удалось найти ссылку для скачивания на странице.')
            return
        print("Успешно 4")
        file_response = session.get(download_link, stream=True)
        if file_response.status_code == 200:
            filename = download_link.split('/')[-1]
            with open(filename, 'wb') as f:
                for chunk in file_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            await message.reply_document(types.InputFile(filename))
            await message.reply('Файл успешно загружен!')
        else:
            await message.reply(f'Не удалось скачать файл. Код ошибки: {file_response.status_code}')
            print("Успешно 5")
    except Exception as e:
        logger.error(f"Ошибка при загрузке файла: {e}")
        await message.reply('Произошла ошибка при загрузке файла. Проверьте ссылку и попробуйте снова.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
