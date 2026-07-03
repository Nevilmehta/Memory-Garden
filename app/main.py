from fastapi import FastAPI

from app.api.routes.chat_routes import router as chat_router
from app.api.routes.memory_routes import router as memory_router
from app.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    description="Long-term memory system for future Jarvis AI.",
    version=settings.APP_VERSION,
)

@app.get("/")
def root():
    return {
        "message": "AI Memory Garden API is running.",
        "phase": "Phase 1 - Memory RAG Foundation",
    }

app.include_router(memory_router)
app.include_router(chat_router)