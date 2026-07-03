from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=3)
    limit: int = Field(default=5, ge=1, le=20)
    min_score: float = Field(default=0.35, ge=0.0, le=1.0)
    category: Optional[str] = None