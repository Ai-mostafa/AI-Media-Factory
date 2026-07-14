from fastapi import FastAPI, Depends
from sqlalchemy import text  # <--- ضفنا دي هنا لحل المشكلة
from sqlalchemy.orm import Session
from app.database import get_db

# إنشاء كائن الـ API الأساسي
app = FastAPI(title="AI Media Factory API", version="1.0")

# صفحة البداية الترحيبية (Root Endpoint)
@app.get("/")
def read_root():
    return {
        "status": "Online",
        "message": "Welcome to AI Media Factory! Your AI Production Studio is active. 🚀"
    }

# نقطة فحص للاتصال بقاعدة البيانات (Database Health Check)
@app.get("/db-check")
def check_database_connection(db: Session = Depends(get_db)):
    try:
        # اختبار استعلام بسيط ومعدل ليتوافق مع SQLAlchemy 2.0
        db.execute(text("SELECT 1"))  # <--- عدلنا دي هنا واستخدمنا text()
        return {"status": "Database is connected successfully! 🟢"}
    except Exception as e:
        return {"status": "Database connection failed! 🔴", "error": str(e)}