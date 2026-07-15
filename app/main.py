from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app import models, routers  # ضفنا الـ routers والـ models هنا

# إنشاء الجداول تلقائياً في قاعدة البيانات
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Media Factory API", version="1.0")

# ربط راوتر الحسابات بالسيرفر
app.include_router(routers.router)

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "message": "Welcome to AI Media Factory! Your AI Production Studio is active. 🚀"
    }

@app.get("/db-check")
def check_database_connection(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "Database is connected successfully! 🟢"}
    except Exception as e:
        return {"status": "Database connection failed! 🔴", "error": str(e)}