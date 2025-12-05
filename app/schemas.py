# app/schemas.py
from typing import List
from pydantic import BaseModel, Field


class RecommendBandRequest(BaseModel):
    """
    Spring에서 FastAPI로 들어오는 요청 바디.

    TODO:
    - user_text, top_k 외에 추가 필드 필요하면 여기에 추가
    """
    user_text: str = Field(..., description="사용자의 음악 취향 텍스트(줄글)")
    top_k: int = Field(5, description="추천 받을 밴드 개수")


class BandItem(BaseModel):
    """
    추천 결과로 반환할 밴드 정보.

    TODO:
    - 밴드 이미지 URL, 대표곡 등 추가 필드가 필요하면 여기에 정의
    """
    id: int
    name: str
    genre_desc: str
    distance: float


class RecommendBandResponse(BaseModel):
    """
    FastAPI → Spring으로 반환할 응답 전체 구조.

    TODO:
    - 모델 정보나 디버깅용 메타데이터를 더 넣고 싶으면 여기에 추가
    """
    model: str
    query_text: str
    bands: List[BandItem]
