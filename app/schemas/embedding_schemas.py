from pydantic import BaseModel
from typing import List


class SingleEmbeddingRequest(BaseModel):
    text: str


class SingleEmbeddingResponse(BaseModel):
    model: str
    embedding: List[float]


class BatchEmbeddingResponse(BaseModel):
    mode: str  # "reset" or "update-missing" 등 동작 구분용
    total_processed: int


class BulkIdsEmbeddingRequest(BaseModel):
    band_description_ids: List[int]


class BulkIdsEmbeddingResponse(BaseModel):
    requested_count: int
    processed_count: int
