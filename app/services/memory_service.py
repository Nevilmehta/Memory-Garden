from app.services.memory_extractor import MemoryExtractor
from app.stores.qdrant_store import QdrantMemoryStore
from app.db.session import SessionLocal
from app.repositories.memory_repository import MemoryRepository

class MemoryService:

    def __init__(self):
        self.memory_store = QdrantMemoryStore()
        self.memory_extractor = MemoryExtractor()
        self.db = SessionLocal()
        self.repository = MemoryRepository(self.db)

    def add_memory(self, memory):
        memory = self.repository.create_memory(
            text = memory.text,
            category = memory.category,
            importance = memory.importance
        )

        self.memory_store.index_memory(
            memory_id=memory.id,
            text=memory.text,
            category=memory.category,
            importance=memory.importance,
            status=memory.status,
            supersedes=memory.supersedes,
            created_at=memory.created_at.isoformat(),
            updated_at=memory.updated_at.isoformat()
        )

        return memory

    def list_memories(self, limit):
        memories = self.repository.list_memories(limit)

        return {
            "count": len(memories),
            "memories": memories,
        }

    def search_memories(self, search):
        results = self.memory_store.search_memories(
            query=search.query,
            limit=search.limit,
            min_score=search.min_score,
            # category=search.category,
        )

        return {
            "query": search.query,
            "results": results,
            "count": len(results),
        }

    def extract_and_store(self, message):
        extraction_result = self.memory_extractor.extract(message)

        extracted_memories = extraction_result["memories"]

        if not extracted_memories:
            return {
                "input_message": message,
                "extracted_memories": [],
                "store_results": [],
                "status": "skipped",
                "message": "No useful long-term memories found.",
            }

        store_results = []

        for extracted_memory in extracted_memories:
            memory = self.repository.create_memory(
                text=extracted_memory["text"],
                category=extracted_memory["category"],
                importance=extracted_memory["importance"],
            )

            self.memory_store.index_memory(
                memory_id=memory.id,
                text=memory.text,
                category=memory.category,
                importance=memory.importance,
                status=memory.status,
                supersedes=memory.supersedes,
                created_at=memory.created_at.isoformat(),
                updated_at=memory.updated_at.isoformat(),
            )

            store_results.append(
                {
                    "id": memory.id,
                    "status": "stored",
                    "category": memory.category,
                }
            )

        return {
            "input_message": message,
            "extracted_memories": extracted_memories,
            "store_results": store_results,
            "status": "completed",
        }

    def reset_memories(self):
        self.repository.reset_memories()

        self.memory_store.reset_memories()
        return {
            "status": "reset"
        }

    def delete_memory(self, memory_id):
        deleted = self.repository.delete_memory(memory_id)

        if not deleted:
            return {
                "status": "not_found"
            }

        self.memory_store.delete_memory(memory_id)

        return {
            "status": "deleted",
            "id": memory_id
        }

    def mark_memory_outdated(self, memory_id):
        memory = self.repository.mark_outdated(memory_id)

        if memory is None:
            return {
                "status": "not_found"
            }

        self.memory_store.mark_memory_outdated(memory_id)

        return {
            "status": "marked_outdated",
            "id": memory_id
        }