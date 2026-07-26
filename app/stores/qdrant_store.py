from datetime import datetime, timezone
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.core.config import settings
from app.services.embedding_service import EmbeddingService


class QdrantMemoryStore:
    def __init__(self):
        self.collection_name = settings.QDRANT_COLLECTION_NAME

        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
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

        if existing_results:
            top_result = existing_results[0]
            top_payload = top_result.payload or {}

            if (
                top_payload.get("status", "active") == "active"
                and top_result.score >= 0.92
            ):
                return {
                    "status": "duplicate",
                    "id": top_result.id,
                    "text": top_payload.get("text"),
                    "category": top_payload.get("category"),
                    "importance": top_payload.get("importance"),
                    "memory_status": top_payload.get("status", "active"),
                    "similarity_score": top_result.score,
                    "message": "A very similar active memory already exists. Memory was not stored again.",
                }

        superseded_memory_ids = []

        if self._looks_like_update(text):
            related_memories = self.find_related_active_memories(
                text=text,
                category=category,
                limit=3,
                min_score=0.45,
            )

            for memory in related_memories:
                self.mark_memory_outdated(memory["id"])
                superseded_memory_ids.append(memory["id"])

        memory_id = str(uuid4())

        now = datetime.now(timezone.utc).isoformat()

        payload = {
            "text": text,
            "category": category,
            "importance": importance,
            "status": "active",
            "created_at": now,
            "updated_at": now,
            "supersedes": superseded_memory_ids,
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
            "memory_status": "active",
            "supersedes": superseded_memory_ids,
        }

    def index_memory(
        self,
        memory_id: str,
        text: str,
        category: str,
        importance: int,
        status: str = "active",
        supersedes: list[str] | None = None,
        created_at: str | None = None,
        updated_at: str | None = None
    ):
        vector = self.embedding_service.embed_text(text)

        payload = {
            "memory_id": memory_id,
            "status": status
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
            "status": "indexed",
            "id": memory_id
        }

    def search_memories(
        self,
        query: str,
        limit: int = 5,
        min_score: float = 0.35,
    ):
        query_vector = self.embedding_service.embed_text(query)

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,
        ).points

        matches = []

        for result in results:
            payload = result.payload or {}

            if payload.get("status") != "active":
                continue

            if result.score < min_score:
                continue

            matches.append(
                {
                    "memory_id": payload["memory_id"],
                    "score": result.score,
                }
            )

        return matches

    def list_memories(self, limit: int = 50):
        results, _ = self.client.scroll(
            collection_name=self.collection_name,
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )

        memories = []

        for point in results:
            payload = point.payload or {}

            memories.append(
                {
                    "id": point.id,
                    "text": payload.get("text"),
                    "category": payload.get("category"),
                    "importance": payload.get("importance"),
                    "memory_status": payload.get("status", "active"),
                    "created_at": payload.get("created_at"),
                    "updated_at": payload.get("updated_at"),
                    "supersedes": payload.get("supersedes", []),
                }
            )

        return memories

    def delete_memory(self, memory_id: str):
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=[memory_id],
        )

        return {
            "status": "deleted",
            "id": memory_id,
        }

    def reset_memories(self):
        self.client.delete_collection(
            collection_name=self.collection_name,
        )

        self._ensure_collection()

        return {
            "status": "reset",
            "message": "All memories were deleted and the collection was recreated.",
        }

    def mark_memory_outdated(self, memory_id: str):
        now = datetime.now(timezone.utc).isoformat()

        self.client.set_payload(
            collection_name=self.collection_name,
            payload={
                "status": "outdated",
                "updated_at": now,
            },
            points=[memory_id]
        )

        return {
            "status": "marked_outdated",
            "id": memory_id,
        }

    def _looks_like_update(self, text:str):
        lower_text = text.lower()

        update_signals = [
            "decided",
            "now",
            "instead",
            "no longer",
            "not anymore",
            "changed",
            "switch",
            "switched",
            "only",
            "prefer",
            "prefers",
            "replaced",
            "rather than",
        ]

        return any(signal in lower_text for signal in update_signals)

    def find_related_active_memories(self, text: str, category: str = "general", limit: int = 3, min_score: float = 0.45):
        query_vector = self.embedding_service.embed_text(text)

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True
        ).points

        related_memories = []

        for result in results:
            payload = result.payload or {}

            if result.score < min_score:
                continue

            if payload.get("status", "active") != "active":
                continue

            if payload.get("category", "general") != category:
                continue

            related_memories.append(
                {
                    "id": result.id,
                    "score": result.score,
                    "text": payload.get("text"),
                    "category": payload.get("category"),
                    "importance": payload.get("importance"),
                }
            )

        return related_memories