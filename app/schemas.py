from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

# ----------------- SCHEMAS FOR SOCIAL ACCOUNTS -----------------
# 1. البيانات المطلوبة لإنشاء حساب جديد
class SocialAccountCreate(BaseModel):
    platform: str = Field(..., example="tiktok")
    username: str = Field(..., example="test_user_1")
    daily_limit: Optional[int] = 5
    proxy: Optional[str] = Field(None, example="http://user:pass@us-proxy-provider.com:8000")
    session_cookies: Optional[dict] = Field(None, example={"sessionid": "abc123xyz..."})

# 2. شكل البيانات اللي بترجع للمستخدم
class SocialAccountResponse(BaseModel):
    id: int
    platform: str
    username: str
    daily_limit: int
    daily_upload_count: int
    last_upload_time: Optional[datetime] = None
    proxy: Optional[str] = None
    session_cookies: Optional[dict] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ----------------- SCHEMAS FOR VIDEOS -----------------
# 3. البيانات المطلوبة لإضافة فيديو للطابور
class VideoCreate(BaseModel):
    title: str = Field(..., example="My Amazing AI Video")
    description: Optional[str] = Field(None, example="Check out this awesome video made by AI!")
    file_path: str = Field(..., example="C:/videos/video_01.mp4")
    account_id: int = Field(..., example=1)

# 4. شكل بيانات الفيديو المرجعة
class VideoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    file_path: str
    status: str
    error_message: Optional[str]
    created_at: datetime
    uploaded_at: Optional[datetime] = None
    account_id: int

    class Config:
        from_attributes = True