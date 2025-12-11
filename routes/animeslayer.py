from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests

router = APIRouter()
path = "/anime"
name = "ANIME API"
type = "public"
url = "https://anslayer.com"

headers = {
    "Client-Id": "android-app2",
    "Client-Secret": "7befba6263cc14c90d2f1d6da2c5cf9b251bfbbd",
    "Accept": "application/json",
    "Accept": "application/*+json",
    "Connection": "Keep-Alive",
    "User-Agent": "okhttp/3.12.12"
}

@router.get("/")
async def get_anime():
    api_url = (
        "https://anslayer.com/anime/public/animes/get-published-animes"
        "?json=%7B%22_offset%22%3A0%2C%22_limit%22%3A30%2C%22_order_by%22%3A%22latest_first%22%2C"
        "%22list_type%22%3A%22latest_updated_episode_new%22%2C%22just_info%22%3A%22Yes%22%7D"
    )

    try:
        res = requests.get(api_url, headers=headers, timeout=10)
        res.raise_for_status()
        return JSONResponse(content=res.json())

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
