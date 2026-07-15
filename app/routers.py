from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
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