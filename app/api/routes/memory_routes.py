from fastapi import APIRouter, Query

from app.schemas.memory_schemas import MemoryCreate, MemorySearch, MessageInput
from app.services.memory_extractor import MemoryExtractor
from app.stores.qdrant_store import QdrantMemoryStore


router = APIRouter(
    prefix="/memories",
    tags=["Memories"],
)

memory_store = QdrantMemoryStore()
memory_extractor = MemoryExtractor()


@router.get("")
def list_memories(limit: int = Query(default=50, ge=1, le=200)):
    memories = memory_store.list_memories(limit=limit)

    return {
        "count": len(memories),
        "memories": memories,
    }


@router.post("")
def add_memory(memory: MemoryCreate):
    result = memory_store.add_memory(
        text=memory.text,
        category=memory.category,
        importance=memory.importance,
    )

    return result


@router.post("/search")
def search_memory(search: MemorySearch):
    results = memory_store.search_memories(
        query=search.query,
        limit=search.limit,
        min_score=search.min_score,
        category=search.category,
    )

    return {
        "query": search.query,
        "results": results,
        "count": len(results),
    }


@router.post("/extract-and-store")
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
        "extracted_memories": extracted_memories,
        "store_results": store_results,
        "status": "completed",
    }


@router.delete("/reset/all")
def reset_memories():
    result = memory_store.reset_memories()

    return result

@router.patch("/{memory_id}/outdated")
def mark_memory_outdated(memory_id: str):
    result = memory_store.mark_memory_outdated(memory_id)

    return result

@router.delete("/{memory_id}")
def delete_memory(memory_id: str):
    result = memory_store.delete_memory(memory_id)

    return result