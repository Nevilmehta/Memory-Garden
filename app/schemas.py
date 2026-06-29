from pydantic import BaseModel, Field
from typing import Optional

class MemoryCreate(BaseModel):
    text: str = Field(..., min_length=3)
    category: Optional[str] = "general"
    importance: Optional[int] = Field(default=5, ge=1, le=10)

class MemorySearch(BaseModel):
    query: str = Field(..., min_length=3)
    limit: int = Field(default=5, ge=1, le=20)

# ------------------------------------------------------------------------

class MessageInput(BaseModel):
    message: str = Field(..., min_length=3)
    