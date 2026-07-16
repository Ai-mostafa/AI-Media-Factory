import sys
import asyncio
import uvicorn

# إجبار الوندوز على استخدام الـ Proactor loop لدعم العمليات الفرعية وفتح المتصفح 🛠️
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app import models, routers

# إنشاء الجداول تلقائياً في قاعدة البيانات
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Media Factory API", version="1.0")

# التأكيد على تطبيق السياسة مع بداية تشغيل التطبيق
@app.on_event("startup")
async def startup_event():
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        print("🟢 Windows Proactor Event Loop Policy Applied successfully (Subprocesses Allowed)!")

# ربط الراوترات
app.include_router(routers.router)
app.include_router(routers.video_router)

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "message": "Welcome to AI Media Factory!"
    }

@app.get("/db-check")
def check_database_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "Database is connected successfully! 🟢"}
    except Exception as e:
        return {"status": "Database connection failed! 🔴", "error": str(e)}

# تشغيل السيرفر من داخل بايثون لضمان تطبيق الـ Policy بالملي 🚀
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)