import httpx
import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1/chat/completions"

async def get_deepseek_response(user_input: str, product_info: str, history: list = []):
    # 1. Định nghĩa System Prompt đóng (Siết chặt phạm vi trả lời)
    system_prompt = f"""
Bạn là chuyên gia tư vấn duy nhất của Toshiko cho dòng ghế massage T90.

[DỮ LIỆU SẢN PHẨM]:
{product_info}

[QUY TẮC BẮT BUỘC]:
1. CHỈ sử dụng thông tin trong [DỮ LIỆU SẢN PHẨM] để trả lời. 
2. Nếu khách hỏi kiến thức ngoài lề (toán học, địa lý, chính trị, hoặc hãng khác), hãy từ chối: "Dạ, em là trợ lý chuyên biệt cho Toshiko T90 nên chỉ hỗ trợ được thông tin về sản phẩm này. Anh/Chị cần tư vấn thêm về tính năng hay giá của T90 không ạ?".
3. Nếu không có thông tin trong dữ liệu, tuyệt đối không tự bịa. Hãy xin lỗi và nhờ khách để lại SĐT.
4. Trả lời bằng tiếng Việt, định dạng Markdown (in đậm các thông số quan trọng).
"""

    # 2. Xây dựng danh sách messages (Giữ lại lịch sử trò chuyện)
    messages = [{"role": "system", "content": system_prompt}]
    
    # Thêm lịch sử (đã được lọc ở chat.py)
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    # Thêm câu hỏi hiện tại của khách
    messages.append({"role": "user", "content": user_input})

    # 3. Cấu hình Payload
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.3, # Giảm độ sáng tạo để AI trả lời chính xác dữ liệu hơn
        "max_tokens": 1024
    }

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    # 4. Gửi Request
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
            return f"❌ Lỗi hệ thống tư vấn: {str(e)}"