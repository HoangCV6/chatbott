import sys
import os

# Đảm bảo Python tìm thấy thư mục 'app'
sys.path.append(os.getcwd())
from app.database import Base, engine
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Product

def seed_product():
    print("Thông báo: Đang kiểm tra và khởi tạo cấu trúc bảng...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Xóa bản ghi cũ nếu có để nạp lại bản đầy đủ nhất (Tùy chọn)
        db.query(Product).filter(Product.name == "Toshiko T90").delete()
        
        t90_full_detail = Product(
            name="Toshiko T90",
            price="27.990.000đ (Giá gốc: 39.990.000đ - Giảm 31%)",
            promotion="""1. Tặng Combo Sắc Đẹp: Thảm massage/Miếng dán massage + Buổi Spa < 500k.
            2. Trả góp lãi suất 0% (Nhắn tin để tư vấn).
            3. Lỗi 1 đổi 1 trong 15 ngày đầu.
            4. Miễn phí 100% vận chuyển và lắp đặt tại nhà.
            5. Trả trước 6 triệu mang ghế về sử dụng ngay.""",
            specifications="""- Công nghệ massage 4D 360° TheraTouch độc quyền.
            - Động cơ MaxDrive-Elite đạt chuẩn EMC.
            - AI Scan Pro+ cá nhân hóa liệu trình.
            - Khung sườn SL 130cm ôm trọn cột sống.
            - Hệ thống 16 túi khí Standard Airbag vùng vai, tay, chân.
            - Chế độ Zero Gravity ngả sâu 154 độ.""",
            description="""Toshiko T90 là trợ lý sức khỏe cá nhân ứng dụng AI. 
            Sử dụng con lăn 4D silicone thử nghiệm >1.000 giờ, mô phỏng tay người: nhào, vỗ, day, miết, bấm huyệt.
            Nhiệt hồng ngoại InfraWarm (35-45°C) thẩm thấu sâu 7mm giúp giãn mao mạch, tăng tuần hoàn máu.
            Công nghệ YogaStretch Function kéo giãn toàn thân 14cm giải phóng áp lực đĩa đệm.
            Cụm LegRevive chăm sóc bàn chân chuyên sâu, tác động huyệt Dũng Tuyền.
            Điều khiển giọng nói SmartVoice AI tiếng Việt phản hồi <3s. 
            Tiện ích: Màn hình LCD 7 inch, Sạc không dây Qi, Loa Bluetooth vòm.
            Chất liệu da Standard PU bền bỉ, kháng khuẩn, chống mốc.
            Phù hợp người già, nhân viên văn phòng, người đau mỏi cần thư giãn.
            Có các chế độ massage chuyên sâu: Shiatsu, Thái, Thụy Điển, Lưng, Vai, Chân.
            Có 10 chế độ cường độ massage tùy chỉnh, phù hợp mọi nhu cầu.""",
        )
        
        db.add(t90_full_detail)
        db.commit()
        print("✅ Đã nạp ĐẦY ĐỦ dữ liệu Toshiko T90 lên Render!")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_product()