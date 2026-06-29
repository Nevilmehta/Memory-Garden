from datetime import datetime, timezone
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from app.embeddings import EmbeddingService


class QdrantMemoryStore:
    def __init__(self):
        self.collection_name = "memory_garden"
        self.client = QdrantClient(
            host="localhost",
            port=6333,
            timeout=60,
            check_compatibility=False,
        )
        self.embedding_service = EmbeddingService()
        self._ensure_collection()

    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        existing_names = [collection.name for collection in collections]

        if self.collection_name not in existing_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_service.vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def add_memory(
        self,
        text: str,
        category: str = "general",
        importance: int = 5,
    ):
        vector = self.embedding_service.embed_text(text)

        existing_results = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=1,
            with_payload=True,
        ).points

        if existing_results and existing_results[0].score >= 0.92:
            existing_memory = existing_results[0]

            return {
                "status": "duplicate",
                "id": existing_memory.id,
                "text": existing_memory.payload.get("text"),
                "category": existing_memory.payload.get("category"),
                "importance": existing_memory.payload.get("importance"),
                "similarity_score": existing_memory.score,
                "message": "A very similar memory already exists. Memory was not stored again.",
            }

        memory_id = str(uuid4())

        payload = {
            "text": text,
            "category": category,
            "importance": importance,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        point = PointStruct(
            id=memory_id,
            vector=vector,
            payload=payload,
        )

        self.client.upsert(
            collection_name=self.collection_name,
            points=[point],
        )

        return {
            "status": "stored",
            "id": memory_id,
            "text": text,
            "category": category,
            "importance": importance,
        }

    def search_memories(self, query: str, limit: int = 5):
        query_vector = self.embedding_service.embed_text(query)

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,
        ).points

        memories = []

        for result in results:
            memories.append(
                {
                    "id": result.id,
                    "score": result.score,
                    "text": result.payload.get("text"),
                    "category": result.payload.get("category"),
                    "importance": result.payload.get("importance"),
                    "created_at": result.payload.get("created_at"),
                }
            )

        return memories