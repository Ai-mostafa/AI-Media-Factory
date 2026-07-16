import sys
import json
import subprocess
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
# استيراد SessionLocal لفتح قاعدة بيانات جديدة داخل الـ Thread
from app.database import get_db, SessionLocal 
from app import models, schemas

router = APIRouter(prefix="/accounts", tags=["Social Accounts"])
video_router = APIRouter(prefix="/videos", tags=["Video Queue"])

# دالة مستقلة لتشغيل عملية الرفع (Independent Background Process) 🚀
def run_independent_uploader(video_id: int, file_path: str, title: str, cookies: dict, proxy: str):
    # نفتح Session جديدة تماماً داخل الـ Thread
    db = SessionLocal() 
    try:
        # تحويل الكوكيز لـ string
        cookies_str = json.dumps(cookies)
        
        print(f"⚡ [Process Manager] Spawning clean python process for Video ID: {video_id}...")
        
        result = subprocess.run(
            [
                sys.executable, 
                "-m", "app.uploader", 
                file_path, 
                title, 
                cookies_str, 
                proxy
            ],
            capture_output=True,
            text=True
        )
        
        # إعادة جلب الفيديو والحساب بنفس الـ Session الجديدة
        video = db.query(models.Video).filter(models.Video.id == video_id).first()
        if not video:
            return

        account = db.query(models.SocialAccount).filter(models.SocialAccount.id == video.account_id).first()
        
        if result.returncode == 0:
            print(f"🟢 [Process Manager] Upload process finished successfully for Video ID: {video_id}")
            video.status = "completed"
            video.uploaded_at = datetime.now()
            if account:
                account.daily_upload_count += 1
                account.last_upload_time = datetime.now()
        else:
            print(f"🔴 [Process Manager] Process failed. Error:\n{result.stderr}")
            video.status = "failed"
            video.error_message = f"Code {result.returncode}: {result.stderr or result.stdout}"
            
        db.commit()
        
    except Exception as proc_err:
        print(f"🚨 [Process Manager] Critical manager error: {proc_err}")
    finally:
        db.close() # إغلاق الـ Session فوراً

# ================= SOCIAL ACCOUNTS ENDPOINTS =================

@router.post("/", response_model=schemas.SocialAccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(account: schemas.SocialAccountCreate, db: Session = Depends(get_db)):
    db_account = db.query(models.SocialAccount).filter(
        models.SocialAccount.platform == account.platform,
        models.SocialAccount.username == account.username
    ).first()
    if db_account:
        raise HTTPException(status_code=400, detail="Account already registered")
    
    new_account = models.SocialAccount(
        platform=account.platform,
        username=account.username,
        daily_limit=account.daily_limit,
        proxy=account.proxy,
        session_cookies=account.session_cookies
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

@router.get("/", response_model=List[schemas.SocialAccountResponse])
def get_accounts(db: Session = Depends(get_db)):
    return db.query(models.SocialAccount).all()

# ================= VIDEO QUEUE ENDPOINTS =================

@video_router.post("/", response_model=schemas.VideoResponse, status_code=status.HTTP_201_CREATED)
def add_video_to_queue(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    account = db.query(models.SocialAccount).filter(models.SocialAccount.id == video.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    new_video = models.Video(
        title=video.title,
        description=video.description,
        file_path=video.file_path,
        account_id=video.account_id
    )
    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return new_video

@video_router.post("/{video_id}/upload", response_model=schemas.VideoResponse)
def upload_video_trigger(video_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
        
    account = db.query(models.SocialAccount).filter(models.SocialAccount.id == video.account_id).first()
    
    # تحديث الحالة إلى Processing
    video.status = "processing"
    db.commit()

    # تشغيل المهمة في الخلفية
    background_tasks.add_task(
        run_independent_uploader,
        video_id=video.id,
        file_path=video.file_path,
        title=video.title,
        cookies=account.session_cookies,
        proxy=account.proxy or "Direct"
    )

    return video