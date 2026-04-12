from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.services.deepseek import get_deepseek_response

router = APIRouter()

@router.post("/send", response_model=schemas.MessageResponse)
async def send_message(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    # 1. Kiểm tra hoặc tạo Session (phiên chat)
    if not request.session_id:
        new_session = models.ChatSession(user_id=request.user_id)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        session_id = new_session.id
    else:
        session_id = request.session_id

    # 2. Lưu tin nhắn của User vào DB
    user_msg = models.Message(session_id=session_id, role="user", content=request.content)
    db.add(user_msg)
    
    # 3. Lấy lịch sử 5 câu gần nhất để AI hiểu ngữ cảnh
    history_db = db.query(models.Message).filter(models.Message.session_id == session_id).order_by(models.Message.created_at.desc()).limit(5).all()
    history_for_ai = [{"role": m.role, "content": m.content} for m in reversed(history_db)]

    # 4. Gọi DeepSeek
    ai_content = await get_deepseek_response(request.content, history=history_for_ai)

    # 5. Lưu phản hồi của AI vào DB
    ai_msg = models.Message(session_id=session_id, role="assistant", content=ai_content)
    db.add(ai_msg)
    
    db.commit()
    db.refresh(ai_msg)
    
    return ai_msg