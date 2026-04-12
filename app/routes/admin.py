from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter()

# Lấy danh sách tất cả người dùng và phiên chat của họ
@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# Xem chi tiết lịch sử chat của một phiên cụ thể
@router.get("/session/{session_id}")
def get_session_detail(session_id: int, db: Session = Depends(get_db)):
    messages = db.query(models.Message).filter(models.Message.session_id == session_id).order_by(models.Message.created_at.asc()).all()
    return messages

# API để Admin trực tiếp trả lời khách hàng
@router.post("/reply")
def admin_reply(session_id: int, content: str, db: Session = Depends(get_db)):
    admin_msg = models.Message(session_id=session_id, role="admin", content=content)
    db.add(admin_msg)
    db.commit()
    return {"status": "success"}