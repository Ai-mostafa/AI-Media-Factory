from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# جدول الحسابات معدل بأقوى أدوات حماية ضد الحظر (Cookies + US Proxy) 🇺🇸🛡️
class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False) # (tiktok, youtube, instagram)
    username = Column(String, nullable=False)
    
    # خانات الأمان والحماية من الحظر (Anti-Ban Fields)
    session_cookies = Column(JSON, nullable=True)    # لتخزين الكوكيز وتجنب كثرة الـ Login
    proxy = Column(String, nullable=True)            # البروكسي الأمريكي (http://user:pass@ip:port)
    daily_limit = Column(Integer, default=5)          # الحد الأقصى المسموح برفع الفيديوهات يومياً
    daily_upload_count = Column(Integer, default=0)   # عدد الفيديوهات المرفوعة اليوم بالفعل
    last_upload_time = Column(DateTime, nullable=True)# لحساب فترات الانتظار العشوائية (Delays)
    is_active = Column(Boolean, default=True)         # حالة الحساب (شغال أم متوقف مؤقتاً لحمايته)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # ربط الحساب بالفيديوهات
    videos = relationship("Video", back_populates="account", cascade="all, delete-orphan")


# جدول الفيديوهات (الطابور)
class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    file_path = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending | processing | completed | failed
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    uploaded_at = Column(DateTime, nullable=True)

    account_id = Column(Integer, ForeignKey("social_accounts.id"), nullable=False)
    account = relationship("SocialAccount", back_populates="videos")