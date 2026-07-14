import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# تحميل المتغيرات من ملف .env
load_dotenv()

# قراءة بيانات الاتصال من البيئة
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# تركيب رابط الاتصال بقاعدة البيانات (Connection String)
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# إنشاء محرك الاتصال (Engine)
engine = create_engine(DATABASE_URL)

# إنشاء جلسات الاتصال (Session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# الأساس اللي هنبني عليه جداول قاعدة البيانات بعد كده (Base Model)
Base = declarative_base()

# دالة للحصول على جلسة اتصال نشطة وقفلها بعد الاستخدام
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print("✅ تم إعداد قاعدة البيانات بنجاح ورابط الاتصال جاهز!")