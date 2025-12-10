# بسم الله الرحمن الرحيم ✨
# API Proxy Fetcher (FastAPI Version)

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests
import json

app = FastAPI()

def fetch_api_via_proxy(api_url: str, proxy_url: str):
    """
    جلب بيانات API عبر بروكسي
    """
    try:
        full_url = f"{proxy_url}/{api_url}"
        print(f"جلب البيانات من: {full_url}")

        response = requests.get(full_url, timeout=10)
        response.raise_for_status()

        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        return {"error": f"خطأ في جلب البيانات: {e}"}

    except json.JSONDecodeError:
        return {
            "error": "JSON Decode Error",
            "raw": response.text[:200]
        }


@app.get("/fetch")
async def fetch(
    api_url: str = Query(..., description="رابط API الأصلي"),
    proxy_url: str = Query("https://rpoxy.apis6.workers.dev", description="رابط البروكسي")
):
    """
    API endpoint:
    /fetch?api_url=xxxxx&proxy_url=xxxxx
    """
    data = fetch_api_via_proxy(api_url, proxy_url)
    return JSONResponse(content=data)


# للران المحلي فقط
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
