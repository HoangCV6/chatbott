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