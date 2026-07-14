from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app import models  # <--- ضفنا دي هنا

# أمر سحري: إنشاء جميع الجداول في قاعدة البيانات تلقائياً لو مش موجودة
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Media Factory API", version="1.0")

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