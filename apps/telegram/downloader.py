import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from aiogram import types
from asgiref.sync import sync_to_async
from apps.telegram.management.commands.bot import dp
from apps.telegram.models import UserDownload

async def download_file_handler(callback_query: types.CallbackQuery, with_license: bool):
    state = dp.current_state(user=callback_query.from_user.id)
    data = await state.get_data()
    file_url = data.get('file_url')

    if file_url:
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            service = Service(executable_path="/path/to/chromedriver")
            browser = webdriver.Chrome(service=service, options=chrome_options)
            browser.get(file_url)

            video_element = browser.find_element(By.CSS_SELECTOR, "div.video-player > video")
            src = video_element.get_attribute("src")
            browser.quit()

            if src:
                response = requests.post('http://127.0.0.1:8000/download/download/', json={'file_url': src})
                if response.status_code == 200:
                    result = response.json()
                    if result["status"] == "success":
                        file_path = result["file_path"]
                        with open(file_path, 'rb') as file:
                            caption = "Ваш файл был загружен с лицензией." if with_license else "Ваш файл был загружен."
                            await callback_query.message.answer_document(file, caption=caption)
                        user = await sync_to_async(UserDownload.objects.get)(user_id=callback_query.from_user.id)
                        user.download_count += 1
                        await sync_to_async(user.save)()
                    else:
                        await callback_query.message.answer(f"Не удалось скачать файл. Ошибка: {result['message']}")
                else:
                    await callback_query.message.answer(f"Не удалось скачать файл. Ошибка: {response.status_code}")
            else:
                await callback_query.message.answer("Не удалось найти видео на указанной странице.")
        except Exception as e:
            await callback_query.message.answer(f"Не удалось скачать файл. Ошибка: {e}")
    else:
        await callback_query.message.answer("Не удалось найти файл. Пожалуйста, попробуйте снова.")
    await callback_query.answer()
