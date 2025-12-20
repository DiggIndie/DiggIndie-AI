from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class BandDescriptionResponse(BaseModel):
    bandId: int
    description: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None
    embedding: Optional[List[float]] = None


class RecommendationRequest(BaseModel):
    bandIds: List[int] = Field(..., min_length=1, description="사용자가 선택한 밴드 ID 목록")
    keyWords: List[str] = Field(default_factory=list, description="사용자가 추가한 키워드 목록")


class RecommendedBand(BaseModel):
    bandId: int
    score: float = Field(..., description="코사인 유사도 점수")


class RecommendationResponse(BaseModel):
    bands: List[RecommendedBand]
