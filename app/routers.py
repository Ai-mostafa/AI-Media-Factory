from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/accounts", tags=["Social Accounts"])

# 1. إنشاء حساب جديد (Create)
@router.post("/", response_model=schemas.SocialAccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(account: schemas.SocialAccountCreate, db: Session = Depends(get_db)):
    # التأكد إن الحساب مش متسجل قبل كده على نفس المنصة
    db_account = db.query(models.SocialAccount).filter(
        models.SocialAccount.platform == account.platform,
        models.SocialAccount.username == account.username
    ).first()
    if db_account:
        raise HTTPException(status_code=400, detail="Account already registered on this platform")
    
    new_account = models.SocialAccount(
        platform=account.platform,
        username=account.username,
        daily_limit=account.daily_limit
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

# 2. عرض كل الحسابات (Read All)
@router.get("/", response_model=List[schemas.SocialAccountResponse])
def get_accounts(db: Session = Depends(get_db)):
    return db.query(models.SocialAccount).all()

# 3. عرض حساب معين بالـ ID (Get by ID)
@router.get("/{account_id}", response_model=schemas.SocialAccountResponse)
def get_account_by_id(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.SocialAccount).filter(models.SocialAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Social account not found")
    return account

# 4. تعديل الحساب (تغيير النشاط أو الحد اليومي)
@router.put("/{account_id}", response_model=schemas.SocialAccountResponse)
def update_account(account_id: int, limit: Optional[int] = None, is_active: Optional[bool] = None, db: Session = Depends(get_db)):
    account = db.query(models.SocialAccount).filter(models.SocialAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Social account not found")
    
    if limit is not None:
        account.daily_limit = limit
    if is_active is not None:
        account.is_active = is_active
        
    db.commit()
    db.refresh(account)
    return account

# 5. محاكاة عملية رفع فيديو (سجل الرفع الآمن)
@router.post("/{account_id}/upload-trigger", response_model=schemas.SocialAccountResponse)
def trigger_upload_simulation(account_id: int, db: Session = Depends(get_db)):
    from datetime import datetime
    account = db.query(models.SocialAccount).filter(models.SocialAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Social account not found")
    
    # فحص الأمان الأول: هل الحساب نشط؟
    if not account.is_active:
        raise HTTPException(status_code=400, detail="This account is deactivated. Activate it first!")
        
    # فحص الأمان الثاني: هل تخطينا الحد اليومي؟
    if account.daily_upload_count >= account.daily_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, 
            detail=f"Safety Lock! Daily limit of {account.daily_limit} uploads reached. Try again tomorrow to avoid ban."
        )
    
    # لو كله تمام، نزود العداد ونسجل الوقت الحالي
    account.daily_upload_count += 1
    account.last_upload_time = datetime.now()
    
    db.commit()
    db.refresh(account)
    return account
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/accounts", tags=["Social Accounts"])
video_router = APIRouter(prefix="/videos", tags=["Video Queue"])

# ================= SOCIAL ACCOUNTS ENDPOINTS =================

@router.post("/", response_model=schemas.SocialAccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(account: schemas.SocialAccountCreate, db: Session = Depends(get_db)):
    db_account = db.query(models.SocialAccount).filter(
        models.SocialAccount.platform == account.platform,
        models.SocialAccount.username == account.username
    ).first()
    if db_account:
        raise HTTPException(status_code=400, detail="Account already registered on this platform")
    
    new_account = models.SocialAccount(
        platform=account.platform,
        username=account.username,
        daily_limit=account.daily_limit,
        proxy=account.proxy,
        session_cookies=account.session_cookies # حفظ الكوكيز في قاعدة البيانات
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

@router.get("/", response_model=List[schemas.SocialAccountResponse])
def get_accounts(db: Session = Depends(get_db)):
    return db.query(models.SocialAccount).all()

@router.get("/{account_id}", response_model=schemas.SocialAccountResponse)
def get_account_by_id(account_id: int, db: Session = Depends(get_db)):
    account = db.query(models.SocialAccount).filter(models.SocialAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Social account not found")
    return account

@router.put("/{account_id}", response_model=schemas.SocialAccountResponse)
def update_account(account_id: int, limit: Optional[int] = None, is_active: Optional[bool] = None, db: Session = Depends(get_db)):
    account = db.query(models.SocialAccount).filter(models.SocialAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Social account not found")
    
    if limit is not None:
        account.daily_limit = limit
    if is_active is not None:
        account.is_active = is_active
        
    db.commit()
    db.refresh(account)
    return account

@router.post("/{account_id}/upload-trigger", response_model=schemas.SocialAccountResponse)
def trigger_upload_simulation(account_id: int, db: Session = Depends(get_db)):
    from datetime import datetime
    account = db.query(models.SocialAccount).filter(models.SocialAccount.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Social account not found")
    
    if not account.is_active:
        raise HTTPException(status_code=400, detail="This account is deactivated. Activate it first!")
        
    if account.daily_upload_count >= account.daily_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, 
            detail=f"Safety Lock! Daily limit of {account.daily_limit} uploads reached. Try again tomorrow."
        )
    
    account.daily_upload_count += 1
    account.last_upload_time = datetime.now()
    
    db.commit()
    db.refresh(account)
    return account


# ================= VIDEO QUEUE ENDPOINTS =================

@video_router.post("/", response_model=schemas.VideoResponse, status_code=status.HTTP_201_CREATED)
def add_video_to_queue(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    account = db.query(models.SocialAccount).filter(models.SocialAccount.id == video.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Target Social Account not found. Add the account first!")
    
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

@video_router.get("/queue", response_model=List[schemas.VideoResponse])
def get_pending_videos(db: Session = Depends(get_db)):
    return db.query(models.Video).filter(models.Video.status == "pending").all()