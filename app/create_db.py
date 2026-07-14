import os
import psycopg2
from dotenv import load_dotenv

# تحميل البيانات من الـ .env
load_dotenv()

# الاتصال بقاعدة البيانات الافتراضية 'postgres' لإنشاء القاعدة الجديدة من خلالها
try:
    conn = psycopg2.connect(
        dbname="postgres",  # بنتصل بالقاعدة الافتراضية أولاً
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # أمر إنشاء قاعدة البيانات الخاصة بمشروعنا
    cursor.execute("CREATE DATABASE ai_media_factory;")
    print("✅ تم إنشاء قاعدة البيانات 'ai_media_factory' بنجاح أخيرًا!")
    
except psycopg2.errors.DuplicateDatabase:
    print("ℹ️ قاعدة البيانات موجودة بالفعل!")
except Exception as e:
    print(f"❌ حدث خطأ أثناء إنشاء قاعدة البيانات: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()