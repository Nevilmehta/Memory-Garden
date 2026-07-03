from fastapi import FastAPI, Query

from app.qdrant_store import QdrantMemoryStore
from app.memory_extractor import MemoryExtractor
from app.answer_generator import AnswerGenerator
from app.schemas import MemoryCreate, MemorySearch, MessageInput, ChatRequest

app = FastAPI(
    title="AI Memory Garden",
    description="Long-term memory system for future Jarvis AI.",
    version="0.1.0",
)

memory_store = QdrantMemoryStore()
memory_extractor = MemoryExtractor()
answer_generator = AnswerGenerator()

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
        limit=search.limit,
        min_score=search.min_score,
        category=search.category
    )

    return {
        "query": search.query,
        "results": results,
        "count": len(results),
    }

# ----------------------------------------------------------------------------

@app.post("/memories/extract-and-store")
def extract_and_store_memory(input_data: MessageInput):
    extraction_result = memory_extractor.extract(input_data.message)

    extracted_memories = extraction_result["memories"]

    if not extracted_memories:
        return {
            "input_message": input_data.message,
            "extracted_memories": [],
            "store_results": [],
            "status": "skipped",
            "message": "No useful long-term memories found.",
        }

    store_results = []

    for extracted_memory in extracted_memories:
        store_result = memory_store.add_memory(
            text=extracted_memory["text"],
            category=extracted_memory["category"],
            importance=extracted_memory["importance"],
        )

        store_results.append(
            {
                "extracted_memory": extracted_memory,
                "store_result": store_result,
            }
        )

    return {
        "input_message": input_data.message,
        "extracted_memory": extracted_memories,
        "store_result": store_results,
        "status": "completed"
    }

# ----------------------------------------------------------------------------

@app.post("/chat")
def chat_with_memory(request: ChatRequest):
    relevant_memories = memory_store.search_memories(
        query=request.question,
        limit=request.limit,
        min_score=request.min_score,
        category=request.category
    )

    answer = answer_generator.generate_answer(
        question=request.question,
        memories=relevant_memories
    )

    return {
        "question": request.question,
        "answer": answer,
        "memories_used": relevant_memories,
        "memory_count": len(relevant_memories)
    }

# ----------------------------------------------------------------------------

@app.get("/memories")
def list_memories(limit: int = Query(50, ge=1, le=200)):
    memories = memory_store.list_memories(limit=limit)

    return {
        "memories": memories,
        "count": len(memories),
    }

@app.delete("/memories/{memory_id}")
def delete_memory(memory_id: str):
    result = memory_store.delete_memory(memory_id=memory_id)

    return result

@app.delete("/memories/reset/all")
def reset_memories():
    result = memory_store.reset_memories()

    return result

# ----------------------------------------------------------------------------
@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "FastAPI is running."
    }

@app.get("/health/qdrant")
def qdrant_health_check():
    collections = memory_store.client.get_collections().collections

    return {
        "status": "ok",
        "collections": [collection.name for collection in collections],
    }