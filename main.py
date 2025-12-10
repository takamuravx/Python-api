# بسم الله الرحمن الرحيم ✨
# API Dynamic Loader (Python Version)

import importlib
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pathlib import Path

app = FastAPI()

# 🌍 متغير عام
t = "https://fantom-devx.vercel.app"

# 📁 مجلد الروتات
ROUTES_DIR = Path(__file__).parent / "routes"
api_list = []

# 🧠 تحميل الروتات ديناميكيًا
def load_routes():
    print("🔄 Loading routes...")
    for file in os.listdir(ROUTES_DIR):
        if file.endswith(".py") and file != "__init__.py":
            module_name = f"routes.{file[:-3]}"

            try:
                module = importlib.import_module(module_name)

                # كل روتر خاصو تكون عندو:
                # path, router, name, type, url, logo
                if hasattr(module, "router") and hasattr(module, "path"):

                    app.include_router(module.router, prefix=module.path)

                    api_list.append({
                        "name": getattr(module, "name", file.replace(".py", "").upper()),
                        "type": getattr(module, "type", "default"),
                        "endpoint": module.path,
                        "url": getattr(module, "url", None),
                        "logo": getattr(module, "logo", None),
                        "status": "Active",
                    })

                    print(f"✅ Loaded: {module.path}")

                else:
                    print(f"⚠️ Missing (path, router) in: {file}")

            except Exception as e:
                print(f"❌ Failed to load {file}: {e}")

load_routes()

# 📜 API LIST
@app.get("/api/list")
async def list_api():
    return JSONResponse(api_list)

# ❌ 404 Handler
@app.exception_handler(404)
async def not_found(_, __):
    return JSONResponse({"error": "Not Found"}, status_code=404)


# 🚀 للران المحلي فقط (Vercel ما كيستعملوش)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9012)
