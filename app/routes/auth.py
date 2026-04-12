from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter()

@router.post("/login")
def login_user(username: str, phone: str, db: Session = Depends(get_db)):
    # Tìm xem user đã tồn tại chưa
    user = db.query(models.User).filter(models.User.phone == phone).first()
    
    if not user:
        # Nếu chưa có thì tạo mới
        user = models.User(username=username, phone=phone)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return {
        "user_id": user.id,
        "username": user.username,
        "is_admin": user.is_admin
    }