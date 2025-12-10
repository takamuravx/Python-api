from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
import json

# إعداد الروتر
router = APIRouter()
path = "/anime"

name = "ANIME API"
type = "public"
url = "https://anslayer.com"
logo = None  # يمكن تحطي رابط شعار إذا كان موجود

# دالة جلب البيانات عبر بروكسي
def fetch_api_via_proxy(api_url: str, proxy_url: str):
    """
    جلب بيانات من API عبر بروكسي
    """
    try:
        full_url = f"{proxy_url}/{api_url}"
        print(f"جلب البيانات من: {full_url}")
        response = requests.get(full_url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0"
        })
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return {"error": f"خطأ في جلب البيانات: {e}"}
    except json.JSONDecodeError:
        return {"error": "خطأ في تحويل JSON", "raw": response.text[:200]}

# endpoint الرئيسي
@router.get("/")
async def get_anime():
    api_url = (
        "https://anslayer.com/anime/public/animes/get-published-animes"
        "?json=%7B%22_offset%22%3A0%2C%22_limit%22%3A30%2C%22_order_by%22%3A%22latest_first%22%2C%22list_type%22%3A%22latest_updated_episode_new%22%2C%22just_info%22%3A%22Yes%22%7D"
    )
    
    # البروكسي: استعملي corsproxy.io لأنه غالباً يعمل أكثر من rpoxy
    proxy_url = "https://corsproxy.io"

    data = fetch_api_via_proxy(api_url, proxy_url)
    return JSONResponse(content=data)
