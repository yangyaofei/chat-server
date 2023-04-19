from typing import List, Tuple

from pydantic import BaseModel


class ChatResponse(BaseModel):
    history: List[Tuple[str, str]] = []
    answer: str


class ChatRequest(BaseModel):
    history: List[Tuple[str, str]] = []
    query: str
    max_length: int = 2048
    top_p: float = 0.7
    temperature: float = 0.95

