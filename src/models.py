"""
Pydantic models for API request/response validation.
"""
from typing import Optional
from pydantic import BaseModel


class CallbackPayload(BaseModel):
    """Payload for AI task callback."""
    taskId: int
    status: str  # "blocked" | "review"
    question: Optional[str] = None
    summary: Optional[str] = None


class TaskMovePayload(BaseModel):
    """Payload for moving a task to a different column."""
    column: str


class CommentPayload(BaseModel):
    """Payload for adding a comment to a task."""
    content: str
    author: str = "user"
