from fastapi import FastAPI

from app.qdrant_store import QdrantMemoryStore
from app.schemas import MemoryCreate, MemorySearch

app = FastAPI(
    title="AI Memory Garden",
    description="Long-term memory system for future Jarvis AI.",
    version="0.1.0",
)

memory_store = QdrantMemoryStore()

@app.get("/")
def root():
    return {
        "message": "AI Memory Garden API is running.",
        "phase": "Phase 1 - Memory RAG Foundation",
    }


@app.post("/memories")
def add_memory(memory: MemoryCreate):
    stored_memory = memory_store.add_memory(
        text=memory.text,
        category=memory.category,
        importance=memory.importance
    )

    return {
        "status": "success",
        "memory": stored_memory
    }

@app.post("/memories/search")
def search_memory(search: MemorySearch):
    results = memory_store.search_memories(
        query=search.query,
        limit=search.limit
    )

    return {
        "query": search.query,
        "results": results
    }