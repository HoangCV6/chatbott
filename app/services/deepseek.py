import httpx
import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1/chat/completions"

async def get_deepseek_response(user_input: str, history: list = []):
    """
    Gửi tin nhắn tới DeepSeek.
    history: Danh sách các tin nhắn cũ để AI nhớ ngữ cảnh.
    """
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    # Cấu hình "System Prompt" để AI biết nó là ai và phục vụ ai
    messages = [
        {"role": "system", "content": "Bạn là một trợ lý ảo thông minh phục vụ khách hàng Việt Nam. Hãy trả lời lịch sự, ngắn gọn và hữu ích bằng tiếng Việt."}
    ]
    
    # Thêm lịch sử trò chuyện vào (nếu có)
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    # Thêm câu hỏi mới nhất của User
    messages.append({"role": "user", "content": user_input})

    payload = {
        "model": "deepseek-chat", # Hoặc "deepseek-reasoner" nếu bạn muốn AI suy nghĩ kỹ hơn
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                DEEPSEEK_BASE_URL, 
                json=payload, 
                headers=headers, 
                timeout=60.0
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"❌ Lỗi khi gọi DeepSeek: {str(e)}"
# Nội dung kiến thức đầy đủ về Toshiko T90
PRODUCT_KNOWLEDGE = """
THÔNG TIN CHI TIẾT TOSHIKO T90:
- Phân khúc: Trung - Cao cấp.
- Giá: 27,990,000đ (Gốc 39,990,000đ).
- Trả trước: Chỉ từ 6 triệu đồng.
- Ưu đãi: Combo Sắc Đẹp (Thảm/miếng dán massage + Spa <500k), Trả góp 0%, 1 đổi 1 trong 15 ngày, Miễn phí vận chuyển/lắp đặt toàn quốc.

CÔNG NGHỆ ĐỘC QUYỀN:
1. Massage 4D 360° TheraTouch: Con lăn silicone độ bền >1.000 giờ, tác động đa chiều (trên-dưới, trái-phải, trong-ngoài), mô phỏng tay người thật.
2. AI Scan Pro+: Cảm biến quang học quét cột sống, lập bản đồ huyệt đạo để cá nhân hóa lực massage.
3. Khung sườn SL 130cm: Dài nhất phân khúc, bao phủ 90% cột sống từ cổ đến đùi.
4. YogaStretch: Kéo giãn toàn thân thêm 14cm, giải phóng áp lực đĩa đệm.
5. InfraWarm: Nhiệt hồng ngoại 35-45°C thấm sâu 7mm vào mô cơ.
6. Toshiko LegRevive: Chăm sóc chuyên sâu bàn chân, tác động huyệt Dũng Tuyền.
7. Zero Gravity: Ngả sâu 154 độ, tư thế không trọng lực giảm áp lực tim và cột sống.
8. Chế độ massage đa dạng: Shiatsu, Thái, Đấm bắp, Lăn, Gõ, Vỗ, Kéo giãn, Không trọng lực.
9. Chế độ tự động: 10 chương trình có sẵn, tùy chỉnh theo nhu cầu cá nhân.
10. Công nghệ túi khí Standard Airbag: 16 túi khí xếp tầng, massage ép, vỗ, kéo giãn toàn thân.
TIỆN ÍCH THÔNG MINH:
- SmartVoice AI: Điều khiển giọng nói tiếng Việt (phản hồi <3s).
- MaxDrive-Elite: Động cơ đạt chuẩn EMC, vận hành siêu mượt.
- Giải trí: Loa Bluetooth vòm, Sạc không dây chuẩn Qi, Màn hình LCD 7 inch.
- Chất liệu: Da Standard PU cao cấp, kháng khuẩn, chống mốc, phù hợp khí hậu VN.
- Màn hình LCD: Hiển thị thông tin massage, nhiệt độ, thời gian, chế độ."""

SYSTEM_PROMPT = f"""
Bạn là Chuyên gia Tư vấn Sức khỏe của Toshiko Việt Nam. 
Hãy sử dụng dữ liệu sau để hỗ trợ khách hàng: {PRODUCT_KNOWLEDGE}

QUY TẮC ỨNG XỬ:
1. Tôn chỉ: "Thân thiện - Chuyên nghiệp - Thấu hiểu".
2. Định dạng: Sử dụng Markdown (in đậm, danh sách) để câu trả lời rõ ràng.
3. Kỹ thuật bán hàng:
   - Khi khách hỏi giá: Nhấn mạnh ưu đãi giảm 31% và chính sách "Trả trước 6 triệu".
   - Khi khách hỏi đau mỏi: Giới thiệu khung SL 130cm và nhiệt InfraWarm.
   - Khi khách là người già: Nhấn mạnh SmartVoice AI (dễ dùng, không cần bấm nút).
4. Câu chốt: Luôn hỏi xem khách có muốn trải nghiệm thử tại showroom gần nhất hoặc tư vấn trả góp không.
"""