from app.database import engine, Base
from app.models import User, ChatSession, Message

def init_db():
    print(" đang khởi tạo các bảng trên Render PostgreSQL...")
    try:
        # Lệnh này sẽ quét các Model và tạo bảng tương ứng trên DB
        Base.metadata.create_all(bind=engine)
        print("✅ Đã tạo bảng thành công!")
    except Exception as e:
        print(f"❌ Lỗi khi tạo bảng: {e}")

if __name__ == "__main__":
    init_db()