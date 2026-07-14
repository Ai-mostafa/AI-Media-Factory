from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from datetime import datetime
from app.database import Base

class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)  # (tiktok, youtube, instagram)
    username = Column(String, nullable=False)
    
    # 🛡️ خانات الأمان والحماية من الحظر (Anti-Ban Fields)
    session_cookies = Column(JSON, nullable=True)     # لتخزين الكوكيز وتجنب كثرة الـ Login
    daily_limit = Column(Integer, default=5)          # الحد الأقصى المسموح برفع الفيديوهات يومياً
    daily_upload_count = Column(Integer, default=0)   # عدد الفيديوهات المرفوعة اليوم بالفعل
    last_upload_time = Column(DateTime, nullable=True) # لحساب فترات الانتظار العشوائية (Delays)
    is_active = Column(Boolean, default=True)         # حالة الحساب (شغال أم متوقف مؤقتاً لحمايته)
    
    created_at = Column(DateTime, default=datetime.utcnow)