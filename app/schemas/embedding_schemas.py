from pydantic import BaseModel
from typing import List


class SingleEmbeddingRequest(BaseModel):
    text: str


class SingleEmbeddingResponse(BaseModel):
    model: str
    embedding: List[float]


class BatchEmbeddingResponse(BaseModel):
    mode: str  # "reset" or "update-missing" 등 동작 구분용
    totalProcessed: int


class BulkIdsEmbeddingRequest(BaseModel):
    bandDescriptionIds: List[int]


class BulkIdsEmbeddingResponse(BaseModel):
    requestedCount: int
    processedCount: int
