# app/api/v1/band_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.band_description_schemas import (
    BandDescriptionResponse,
    RecommendationRequestV1,
    RecommendationRequestV2,
    RecommendationRequestV3,
    RecommendationResponse,
    RecommendedBand,
)
from app.services.band_description_service import fetch_band_description
from app.services.recommendation_service import recommend_bands_v1, recommend_bands_v2, recommend_bands_v3

router = APIRouter(
    prefix="/bands",
    tags=["bands"],
)


@router.post("/recommendations/update/v1", response_model=RecommendationResponse)
async def update_recommendations_v1(
    body: RecommendationRequestV1,
    db: Session = Depends(get_db),
):
    """
    [V1] 사용자가 선택한 밴드 ID 목록을 기반으로 추천 밴드 상위 3개 반환.
    
    알고리즘:
    - 1개 선택: 해당 임베딩 그대로 사용
    - 2개 선택: 단순 평균
    - 3개 이상: K-means 클러스터링(k=3) + 가중 평균
    - 코사인 유사도로 모든 밴드와 비교
    - 유사도 높은 상위 3개 밴드 반환
    """
    try:
        recommendations = recommend_bands_v1(db, body.bandIds, top_k=3)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"추천 생성 실패: {e}")
    
    bands = [
        RecommendedBand(
            bandId=rec["band_id"],
            score=round(rec["score"], 4),
            bandName=rec["band_name"],
            imageUrl=rec["image_url"],
            bandMusic=rec["band_music"],
            keywords=rec["keywords"],
        )
        for rec in recommendations
    ]
    
    return RecommendationResponse(bands=bands)


@router.post("/recommendations/update/v2", response_model=RecommendationResponse)
async def update_recommendations_v2(
    body: RecommendationRequestV2,
    db: Session = Depends(get_db),
):
    """
    [V2] 밴드 + 키워드 기반 추천.
    
    알고리즘:
    - 밴드 임베딩으로 사용자 벡터 생성 (V1과 동일)
    - 키워드를 임베딩하여 키워드 벡터 생성
    - 유사도 기반으로 t 값 동적 계산
    - Slerp(구면 선형 보간)로 사용자 벡터에 키워드 방향 반영
    - 코사인 유사도로 모든 밴드와 비교
    - 유사도 높은 상위 3개 밴드 반환
    """
    try:
        recommendations = recommend_bands_v2(
            db=db,
            band_ids=body.bandIds,
            keyword_ids=body.keywords,
            top_k=3,
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"추천 생성 실패: {e}")
    
    bands = [
        RecommendedBand(
            bandId=rec["band_id"],
            score=round(rec["score"], 4),
            bandName=rec["band_name"],
            imageUrl=rec["image_url"],
            bandMusic=rec["band_music"],
            keywords=rec["keywords"],
        )
        for rec in recommendations
    ]
    
    return RecommendationResponse(bands=bands)


@router.post("/recommendations/update/v3", response_model=RecommendationResponse)
async def update_recommendations_v3(
    body: RecommendationRequestV3,
    db: Session = Depends(get_db),
):
    """
    [V3] 클러스터별 키워드 반영 추천.
    
    알고리즘:
    - K-means 클러스터링(k=3)으로 3개의 centroid 생성
    - 각 centroid에 키워드 벡터를 Slerp로 적용
    - 조정된 각 centroid에서 가장 유사한 밴드 1개씩 선택
    - 총 3개의 다양한 밴드 반환
    
    ※ 밴드가 3개 미만이면 V2로 폴백
    """
    try:
        recommendations = recommend_bands_v3(
            db=db,
            band_ids=body.bandIds,
            keyword_ids=body.keywords,
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"추천 생성 실패: {e}")
    
    bands = [
        RecommendedBand(
            bandId=rec["band_id"],
            score=round(rec["score"], 4),
            bandName=rec["band_name"],
            imageUrl=rec["image_url"],
            bandMusic=rec["band_music"],
            keywords=rec["keywords"],
        )
        for rec in recommendations
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
