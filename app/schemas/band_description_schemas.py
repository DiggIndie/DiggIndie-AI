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


class RecommendationRequestV1(BaseModel):
    """V1 추천 요청 스키마 (밴드 ID만 사용)"""
    bandIds: List[int] = Field(..., min_length=1, description="사용자가 선택한 밴드 ID 목록")


class RecommendationRequestV2(BaseModel):
    """V2 추천 요청 스키마 (밴드 ID + 키워드 ID 사용)"""
    bandIds: List[int] = Field(..., min_length=1, description="사용자가 선택한 밴드 ID 목록")
    keywords: List[int] = Field(default_factory=list, description="사용자가 선택한 키워드 ID 목록")


class RecommendedBand(BaseModel):
    bandId: int
    score: float = Field(..., description="코사인 유사도 점수")
    bandName: Optional[str] = None
    imageUrl: Optional[str] = None
    bandMusic: Optional[str] = None
    keywords: List[str] = Field(default_factory=list, description="밴드 키워드 목록")


class RecommendationResponse(BaseModel):
    bands: List[RecommendedBand]
