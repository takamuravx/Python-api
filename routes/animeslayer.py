from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
import random

router = APIRouter()
path = "/anime"
name = "ANIME API"
type = "public"
url = "https://anslayer.com"

# 📌 بروكسياتك كاملين
PROXIES = [
    {"name": "caliph", "url": "https://cors.caliph.my.id/"},
    {"name": "eu", "url": "https://cors.eu.org/"},
    {"name": "square", "url": "https://square.proxyserver2.workers.dev/"},
    {"name": "rpoxy", "url": "https://rpoxy.apis6.workers.dev/"},
    {"name": "aged", "url": "https://aged-hill-ab3a.apis4.workers.dev/"},
    {"name": "wave", "url": "https://plain-wave-6f5f.apis1.workers.dev/"},
    {"name": "hill", "url": "https://young-hill-815e.apis3.workers.dev/"},
    {"name": "icy", "url": "https://icy-morning-72e2.apis2.workers.dev/"},
    {"name": "surf", "url": "https://young-surf-7189.apis7.workers.dev/"},
    {"name": "fazri", "url": "https://cors.fazri.workers.dev/"},
    {"name": "spring", "url": "https://spring-night-57a1.3540746063.workers.dev/"},
    {"name": "sizable", "url": "https://cors.sizable.workers.dev/"},
    {"name": "jiashu", "url": "https://jiashu.1win.eu.org/"},
]

# 📌 User-Agents واقعيين
ANDROID_USER_AGENTS = [
    "okhttp/3.12.12",
    "okhttp/3.12.13",
    "Dalvik/2.1.0 (Linux; U; Android 10)",
    "Dalvik/2.1.0 (Linux; U; Android 11)",
    "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 Chrome/110.0.0.0 Mobile Safari/537.36",
]


# 📌 هيدر واقعي 100% بحال التطبيق ديال Android
def generate_real_headers():
    return {
        "User-Agent": random.choice(ANDROID_USER_AGENTS),
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive",
        "Host": "anslayer.com",

        "Client-Id": "android-app2",
        "Client-Secret": "7befba6263cc14c90d2f1d6da2c5cf9b251bfbbd",

        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "en-US",
        "Platform": "android",
    }


# 🎯 الدالة لي كتجرب البروكسيات كاملين حتى ينجح الطلب
def fetch_with_all_proxies(api_url):
    headers = generate_real_headers()

    for proxy in PROXIES:
        proxy_url = proxy["url"] + api_url
        print(f"🔄 تجربة البروكسي: {proxy['name']}  -->  {proxy_url}")

        try:
            res = requests.get(proxy_url, headers=headers, timeout=12)

            if res.status_code == 200:
                print(f"✅ نجاح عبر البروكسي: {proxy['name']}")
                return {
                    "success": True,
                    "proxy_used": proxy["name"],
                    "data": res.json()
                }

        except Exception as e:
            print(f"❌ فشل عبر: {proxy['name']} | {e}")

    return {"success": False, "error": "فشلت جميع البروكسيات"}


# 🎉 Endpoint الرئيسي
@router.get("/")
async def get_anime():
    url = (
        "https://anslayer.com/anime/public/animes/get-published-animes"
        "?json=%7B%22_offset%22%3A0%2C%22_limit%22%3A30%2C%22_order_by%22%3A%22latest_first%22%2C"
        "%22list_type%22%3A%22filter%22%2C%22anime_name%22%3A%22na%22%2C%22just_info%22%3A%22Yes%22%7D"
    )

    result = fetch_with_all_proxies(url)
    return JSONResponse(content=result)
