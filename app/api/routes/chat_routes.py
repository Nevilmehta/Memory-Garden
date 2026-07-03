from fastapi import APIRouter

from app.schemas.chat_schemas import ChatRequest
from app.services.answer_generator import AnswerGenerator
from app.stores.qdrant_store import QdrantMemoryStore


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

memory_store = QdrantMemoryStore()
answer_generator = AnswerGenerator()


@router.post("")
def chat_with_memory(request: ChatRequest):
    relevant_memories = memory_store.search_memories(
        query=request.question,
        limit=request.limit,
        min_score=request.min_score,
        category=request.category,
    )

    answer = answer_generator.generate_answer(
        question=request.question,
        memories=relevant_memories,
    )

    return {
        "question": request.question,
        "answer": answer,
        "memories_used": relevant_memories,
        "memory_count": len(relevant_memories),
    }