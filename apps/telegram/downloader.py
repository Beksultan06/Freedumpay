import requests
import os

def download_file(file_url):
    local_filename = file_url.split('/')[-1]
    local_path = os.path.join("C:\\Users\\USER\\Desktop\\Freedumpay\\downloads", local_filename)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Отправляем запрос на скачивание файла
    response = requests.get(file_url, headers=headers, stream=True)

    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return local_path
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
        return None
