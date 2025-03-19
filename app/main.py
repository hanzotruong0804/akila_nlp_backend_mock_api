from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat

app = FastAPI(title="Akila NLP backend Chat Mock API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Đăng ký router chat
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {
        "message": "Akila NLP backend Chat Mock API!",
    }
