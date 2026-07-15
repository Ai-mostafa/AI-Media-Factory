from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime

# البيانات المطلوبة عند إنشاء حساب جديد
class SocialAccountCreate(BaseModel):
    platform: str = Field(..., example="tiktok")
    username: str = Field(..., example="test_user_1")
    daily_limit: Optional[int] = 5

# شكل البيانات اللي هترجع للمستخدم
class SocialAccountResponse(BaseModel):
    id: int
    platform: str
    username: str
    daily_limit: int
    daily_upload_count: int
    last_upload_time: Optional[datetime] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True