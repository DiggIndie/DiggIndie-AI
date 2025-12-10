from pydantic import BaseModel
from typing import List

class SingleEmbeddingRequest(BaseModel):
    text: str


class SingleEmbeddingResponse(BaseModel):
    model: str
    embedding: List[float]
