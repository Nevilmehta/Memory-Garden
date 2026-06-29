from fastapi import FastAPI

from app.qdrant_store import QdrantMemoryStore
from app.memory_extractor import MemoryExtractor
from app.schemas import MemoryCreate, MemorySearch, MessageInput

app = FastAPI(
    title="AI Memory Garden",
    description="Long-term memory system for future Jarvis AI.",
    version="0.1.0",
)

memory_store = QdrantMemoryStore()
memory_extractor = MemoryExtractor()

@app.get("/")
def root():
    return {
        "message": "AI Memory Garden API is running.",
        "phase": "Phase 1 - Memory RAG Foundation",
    }

# --------------------------------------------------------------------------

@app.post("/memories")
def add_memory(memory: MemoryCreate):
    result = memory_store.add_memory(
        text=memory.text,
        category=memory.category,
        importance=memory.importance,
    )

    return result

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

# ----------------------------------------------------------------------------

@app.post("/memories/extract-and-store")
def extract_and_store_memory(input_data: MessageInput):
    extracted_memory = memory_extractor.extract(input_data.message)

    if not extracted_memory["should_store"]:
        return {
            "input_message": input_data.message,
            "extracted_memory": extracted_memory,
            "store_result": {
                "status": "skipped",
                "message": "No useful long-term memory found.",
            },
        }

    store_result = memory_store.add_memory(
        text=extracted_memory["text"],
        category=extracted_memory["category"],
        importance=extracted_memory["importance"],
    )

    return {
        "input_message": input_data.message,
        "extracted_memory": extracted_memory,
        "store_result": store_result,
    }

