from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat
from app.routes import chat, auth # Thêm auth
from app.routes import chat, auth, admin

app = FastAPI(title="Toshiko Chatbot AI")
# backend/app/main.py
origins = [
    "http://localhost:3000",
    "https://ten-app-cua-ban.vercel.app", # Thêm link Vercel vừa tạo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Thay vì ["*"] để bảo mật hơn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
def root():
    return {"message": "Backend AI is running!"}