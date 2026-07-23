from fastapi import APIRouter, Query

from app.schemas.memory_schemas import MemoryCreate, MemorySearch, MessageInput
from app.services.memory_extractor import MemoryExtractor
from app.stores.qdrant_store import QdrantMemoryStore
from app.services.memory_service import MemoryService

memory_service = MemoryService()

router = APIRouter(
    prefix="/memories",
    tags=["Memories"],
)

@router.get("")
def list_memories(limit: int = Query(default=50, ge=1, le=200)):
    return memory_service.list_memories(limit)

@router.post("")
def add_memory(memory: MemoryCreate):
    return memory_service.add_memory(memory)

@router.post("/search")
def search_memory(search: MemorySearch):
    return memory_service.search_memories(search)

@router.post("/extract-and-store")
def extract_and_store_memory(input_data: MessageInput):
    return memory_service.extract_and_store(
        input_data.message
    )

@router.delete("/reset/all")
def reset_memories():
    return memory_service.reset_memories()

@router.patch("/{memory_id}/outdated")
def mark_memory_outdated(memory_id: str):
    return memory_service.mark_memory_outdated(memory_id)

@router.delete("/{memory_id}")
def delete_memory(memory_id: str):
    return memory_service.delete_memory(memory_id)