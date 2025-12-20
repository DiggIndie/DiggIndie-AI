# app/api/v1/band_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.band_description_schemas import (
    BandDescriptionResponse,
    RecommendationRequest,
    RecommendationResponse,
    RecommendedBand,
)
from app.services.band_description_service import fetch_band_description
from app.services.recommendation_service import recommend_bands

router = APIRouter(
    prefix="/bands",
    tags=["bands"],
)


@router.post("/recommendations/update", response_model=RecommendationResponse)
async def update_recommendations(
    body: RecommendationRequest,
    db: Session = Depends(get_db),
):
    """
    사용자가 선택한 밴드 ID 목록을 기반으로 추천 밴드 상위 3개 반환.
    
    - K-means 클러스터링(k=3)으로 사용자 취향 벡터 생성
    - 코사인 유사도로 모든 밴드와 비교
    - 유사도 높은 상위 3개 밴드 반환
    """
    try:
        recommendations = recommend_bands(db, body.bandIds, top_k=3)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"추천 생성 실패: {e}")
    
    bands = [
        RecommendedBand(bandId=band_id, score=round(score, 4))
        for band_id, score in recommendations
    ]
    
    return RecommendationResponse(bands=bands)


@router.get("/{band_id}", response_model=BandDescriptionResponse)
async def read_band_description(
    band_id: int,
    db: Session = Depends(get_db),
):
    """
    특정 band_id의 row를 읽어서 embedding까지 반환하는 확인용 API
    """
    result = fetch_band_description(db, band_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Band not found")
    return result
