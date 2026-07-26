from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.db.models import Memory

class MemoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_memory(self, text: str, category: str, importance: int, supersedes: list[str]|None=None):
        memory = Memory(
            text=text,
            category=category,
            importance=importance,
            status="active",
            supersedes=supersedes or []
        )

        self.db.add(memory)
        self.db.commit()
        self.db.refresh(memory)

        return memory

    def list_memories(self, limit: int = 50):
        return (
            self.db.query(Memory)
            .order_by(Memory.created_at.desc())
            .limit(limit)
            .all()
        )

    def get_memory(self, memory_id: str):
        return ( self.db.query(Memory).filter(Memory.id == memory_id).first())

    def mark_outdated(self, memory_id: str):
        memory = self.get_memory(memory_id)
        if not memory:
            return None

        memory.status = "outdated"
        memory.updated_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(memory)

        return memory

    def delete_memory(self, memory_id: str):
        memory = self.get_memory(memory_id)
        if not memory:
            return False

        self.db.delete(memory)
        self.db.commit()

        return True

    def reset_memories(self):
        self.db.query(Memory).delete()
        self.db.commit()

    def get_memories_by_ids(self, memory_ids):
        memories = (
            self.db.query(Memory)
            .filter(Memory.id.in_(memory_ids))
            .all()
        )