from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
import random

router = APIRouter()
path = "/anime"
name = "ANIME API"
type = "public"
url = "https://anslayer.com"

# قائمة User-Agents باش كل طلب يبان مختلف (بحال تطبيق حقيقي)
ANDROID_USER_AGENTS = [
    "okhttp/3.12.12",
    "okhttp/3.12.13",
    "Dalvik/2.1.0 (Linux; U; Android 10)",
    "Dalvik/2.1.0 (Linux; U; Android 11)",
    "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 Chrome/110.0.0.0 Mobile Safari/537.36",
]

def generate_real_headers():
    return {
        "User-Agent": random.choice(ANDROID_USER_AGENTS),
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive",
        "Host": "anslayer.com",

        # مهمّين باش Cloudflare يسمح للطلب
        "Client-Id": "android-app2",
        "Client-Secret": "7befba6263cc14c90d2f1d6da2c5cf9b251bfbbd",

        # يزيد المصداقية
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "en-US",
        "Platform": "android",
    }

@router.get("/")
async def get_anime():
    try:
        url = (
            "https://anslayer.com/anime/public/animes/get-published-animes"
            "?json=%7B%22_offset%22%3A0%2C%22_limit%22%3A30%2C%22_order_by%22%3A%22latest_first%22%2C"
            "%22list_type%22%3A%22filter%22%2C%22anime_name%22%3A%22na%22%2C%22just_info%22%3A%22Yes%22%7D"
        )

        headers = generate_real_headers()
        print("📌 Sending request with headers:", headers)

        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()

        return JSONResponse(content=res.json())

    except Exception as e:
        return JSONResponse(
            content={"error": "فشل الطلب", "details": str(e)}, 
            status_code=500
        )
