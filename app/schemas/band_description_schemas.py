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


class RecommendationRequestV3(BaseModel):
    """V3 추천 요청 스키마 (클러스터별 키워드 반영, 밴드 3개 이상 필요)"""
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


# ============================================================
# 최종 추천 API 응답 스키마 (POST /api/bands/recommendations/update)
# ============================================================

class TopTrackResponse(BaseModel):
    """TopTrack 응답 스키마"""
    title: str
    externalUrl: str


class RecommendedBandFinal(BaseModel):
    """최종 추천 밴드 응답 스키마 (TopTrack 포함)"""
    bandId: int
    score: float = Field(..., description="코사인 유사도 점수")
    bandName: Optional[str] = None
    imageUrl: Optional[str] = None
    topTrack: Optional[TopTrackResponse] = None
    keywords: List[str] = Field(default_factory=list, description="밴드 키워드 목록")


class RecommendationPayload(BaseModel):
    """추천 응답 payload"""
    bands: List[RecommendedBandFinal]


class FinalRecommendationResponse(BaseModel):
    """최종 추천 API 응답 스키마 (Spring 응답 형식에 맞춤)"""
    statusCode: int = 200
    isSuccess: bool = True
    message: str = "추천 밴드 업데이트 API"
    payload: RecommendationPayload
