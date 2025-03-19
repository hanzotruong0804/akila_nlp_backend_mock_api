
from fastapi import FastAPI
from app.routers import chat

app = FastAPI(title="Akila NLP backend Chat Mock API")

# Đăng ký router chat
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {
        "message": "Akila NLP backend Chat Mock API!",
    }
