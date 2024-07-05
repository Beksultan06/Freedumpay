from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

def download_file(file_url):
    # Настройки для скачивания файла без запроса на сохранение
    chrome_options = Options()
    prefs = {"download.default_directory": "C:\\Users\\USER\\Desktop\\Freedumpay\\downloads",  # Укажите правильный путь к директории загрузки
             "profile.default_content_settings.popups": 0,
             "directory_upgrade": True}
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Укажите правильный путь к вашему chromedriver
    service = Service('C:\\path\\to\\chromedriver.exe')  # Укажите правильный путь к chromedriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(file_url)
        time.sleep(10)  # Подождите некоторое время, чтобы завершить скачивание
    finally:
        driver.quit()

    # Проверка существования файла
    file_name = file_url.split('/')[-1]  # Предполагаемый формат файла, измените при необходимости
    file_path = os.path.join("C:\\Users\\USER\\Desktop\\Freedumpay\\downloads", file_name)
    if os.path.exists(file_path):
        return file_path
    else:
        return None