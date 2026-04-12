from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Lấy URL từ .env
db_url = os.getenv("DATABASE_URL")

# Nếu trong .env quên chưa thêm, đoạn code này sẽ tự kiểm tra và thêm vào
if "sslmode" not in db_url:
    if "?" in db_url:
        db_url += "&sslmode=require"
    else:
        db_url += "?sslmode=require"

engine = create_engine(db_url)

try:
    with engine.connect() as connection:
        print("✅ Kết nối Render PostgreSQL thành công với SSL!")
except Exception as e:
    print(f"❌ Kết nối thất bại. Lỗi: {e}")