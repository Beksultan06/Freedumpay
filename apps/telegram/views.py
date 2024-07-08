import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json

@csrf_exempt
def download_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            file_url = data.get("file_url")
            print(file_url,'file_url vievws')
            if file_url:
                local_filename = file_url.split('/')[-1]
                local_path = os.path.join("downloads", local_filename)

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }

                response = requests.get(file_url, stream=True, headers=headers)
                if response.status_code == 200:
                    with open(local_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    return JsonResponse({"status": "success", "file_path": local_path})
                else:
                    return JsonResponse({"status": "error", "message": f"Failed to download file. Status code: {response.status_code}"})
            else:
                return JsonResponse({"status": "error", "message": "No file URL provided"})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method."})
