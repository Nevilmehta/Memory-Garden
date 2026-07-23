from app.services.memory_extractor import MemoryExtractor
from app.stores.qdrant_store import QdrantMemoryStore

class MemoryService:

    def __init__(self):
        self.memory_store = QdrantMemoryStore()
        self.memory_extractor = MemoryExtractor()

    def add_memory(self, memory):
        return self.memory_store.add_memory(
            text=memory.text,
            category=memory.category,
            importance=memory.importance,
        )

    def list_memories(self, limit):
        memories = self.memory_store.list_memories(limit=limit)

        return {
            "count": len(memories),
            "memories": memories,
        }

    def search_memory(self, search):
        results = self.memory_store.search_memories(
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

            store_result = self.memory_store.add_memory(
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
            "input_message": message,
            "extracted_memories": extracted_memories,
            "store_results": store_results,
            "status": "completed",
        }

    def reset_memories(self):
        return self.memory_store.reset_memories()

    def delete_memory(self, memory_id):
        return self.memory_store.delete_memory(memory_id)

    def mark_memory_outdated(self, memory_id):
        return self.memory_store.mark_memory_outdated(memory_id)