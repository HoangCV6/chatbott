from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.services.deepseek import get_deepseek_response

router = APIRouter()

@router.post("/send", response_model=schemas.MessageResponse)
async def send_message(request: schemas.ChatRequest, db: Session = Depends(get_db)):
    # 1. Kiểm tra hoặc tạo Session
    if not request.session_id:
        new_session = models.ChatSession(user_id=request.user_id)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        session_id = new_session.id
    else:
        session_id = request.session_id

    # 2. Lấy THÔNG TIN SẢN PHẨM T90 từ Database (MỚI)
    product = db.query(models.Product).filter(models.Product.name == "Toshiko T90").first()
    
    if product:
        product_context = f"""
        THÔNG TIN SẢN PHẨM:
        - Tên: {product.name}
        - Giá: {product.price}
        - Khuyến mãi: {product.promotion}
        - Thông số: {product.specifications}
        - Chi tiết: {product.description}
        """
    else:
        product_context = "Thông tin sản phẩm hiện đang cập nhật."

    # 3. Lưu tin nhắn của User vào DB
    user_msg = models.Message(session_id=session_id, role="user", content=request.content)
    db.add(user_msg)
    db.flush() # Dùng flush để có dữ liệu gửi đi trước khi commit

    # 4. Lấy lịch sử 5 câu gần nhất
    history_db = db.query(models.Message).filter(models.Message.session_id == session_id).order_by(models.Message.created_at.desc()).limit(5).all()
    history_for_ai = [{"role": m.role, "content": m.content} for m in reversed(history_db)]

    # 5. Gọi DeepSeek và truyền kèm PRODUCT_INFO (SỬA Ở ĐÂY)
    # Hàm get_deepseek_response trong file deepseek.py cần được sửa để nhận thêm tham số này
    ai_content = await get_deepseek_response(
        user_input=request.content, 
        product_info=product_context, 
        history=history_for_ai
    )

    # 6. Lưu phản hồi của AI vào DB
    ai_msg = models.Message(session_id=session_id, role="assistant", content=ai_content)
    db.add(ai_msg)
    
    db.commit()
    db.refresh(ai_msg)
    
    return ai_msg