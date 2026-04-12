import asyncio
from app.services.deepseek import get_deepseek_response

async def main():
    print("🤖 Đang hỏi DeepSeek...")
    question = "Chào bạn, bạn có thể giúp tôi xây dựng chatbot bằng Python không?"
    answer = await get_deepseek_response(question)
    print(f"\nUser: {question}")
    print(f"AI: {answer}")

if __name__ == "__main__":
    asyncio.run(main()) 