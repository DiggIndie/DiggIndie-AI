# app/api/v1/band_routes.py
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.auth import get_current_user_external_id
from app.core.exceptions import (
    NoBandSelectedException,
    NoKeywordSelectedException,
    MemberNotFoundException,
)
from app.schemas.band_description_schemas import (
    BandDescriptionResponse,
    RecommendationRequestV1,
    RecommendationRequestV2,
    RecommendationRequestV3,
    RecommendationResponse,
    RecommendedBand,
    FinalRecommendationResponse,
    RecommendationPayload,
    RecommendedBandFinal,
    TopTrackResponse,
)
from app.services.band_description_service import fetch_band_description
from app.services.recommendation_service import recommend_bands_v1, recommend_bands_v2, recommend_bands_v3
from app.repositories.band_description_repository import (
    get_member_by_external_id,
    get_member_band_ids,
    get_member_keyword_ids,
    delete_band_recommends,
    save_band_recommends,
    get_band_recommends_with_details,
)

logger = logging.getLogger(__name__)

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


# ============================================================
# 최종 추천 API (JWT 인증 필요)
# ============================================================

@router.post("/recommendations/update", response_model=FinalRecommendationResponse)
async def update_recommendations_final(
    external_id: str = Depends(get_current_user_external_id),
    db: Session = Depends(get_db),
):
    """
    [최종 추천 API] JWT 인증 기반 추천 밴드 업데이트 및 반환.
    
    흐름:
    1. JWT에서 externalId 추출
    2. Member 조회 -> memberId
    3. MemberBand, MemberKeyword 조회 -> bandIds, keywordIds
    4. recommend_bands_v3 호출 (밴드 3개 미만 시 V2 폴백)
    5. BandRecommend 테이블에 저장 (기존 삭제 후 새로 저장)
    6. Band + TopTrack + Keyword 정보와 함께 반환
    """
    logger.info(f"[최종 추천 API] 요청 시작 - externalId: {external_id}")
    
    # 1. Member 조회
    member = get_member_by_external_id(db, external_id)
    if not member:
        logger.warning(f"[최종 추천 API] 회원 없음 - externalId: {external_id}")
        raise MemberNotFoundException()
    
    member_id = member.id
    logger.info(f"[최종 추천 API] 회원 조회 성공 - memberId: {member_id}")
    
    # 2. 사용자가 선택한 밴드 조회
    band_ids = get_member_band_ids(db, member_id)
    if not band_ids:
        logger.warning(f"[최종 추천 API] 선택한 밴드 없음 - memberId: {member_id}")
        raise NoBandSelectedException()
    
    logger.info(f"[최종 추천 API] 선택한 밴드 ({len(band_ids)}개): {band_ids}")
    
    # 3. 사용자가 선택한 키워드 조회
    keyword_ids = get_member_keyword_ids(db, member_id)
    if not keyword_ids:
        logger.warning(f"[최종 추천 API] 선택한 키워드 없음 - memberId: {member_id}")
        raise NoKeywordSelectedException()
    
    logger.info(f"[최종 추천 API] 선택한 키워드 ID ({len(keyword_ids)}개): {keyword_ids}")
    
    # 4. V3 추천 로직 실행
    try:
        recommendations = recommend_bands_v3(
            db=db,
            band_ids=band_ids,
            keyword_ids=keyword_ids,
        )
        logger.info(f"[최종 추천 API] 추천 결과: {len(recommendations)}개 밴드")
    except ValueError as ve:
        logger.error(f"[최종 추천 API] 추천 로직 ValueError: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"[최종 추천 API] 추천 로직 오류: {e}")
        raise HTTPException(status_code=500, detail=f"추천 생성 실패: {e}")
    
    # 5. BandRecommend 저장 (기존 삭제 후 새로 저장)
    deleted_count = delete_band_recommends(db, member_id)
    logger.info(f"[최종 추천 API] 기존 추천 삭제: {deleted_count}개")
    
    # 추천 결과를 저장용 형식으로 변환
    recs_to_save = [
        {"band_id": rec["band_id"], "score": rec["score"]}
        for rec in recommendations
    ]
    
    saved_recommends = save_band_recommends(db, member_id, recs_to_save)
    logger.info(f"[최종 추천 API] 새 추천 저장: {len(saved_recommends)}개")
    
    # 6. 커밋
    db.commit()
    
    # 7. 상세 정보 조회
    band_details = get_band_recommends_with_details(db, member_id)
    logger.info(f"[최종 추천 API] 상세 정보 조회 완료")
    
    # 8. 응답 생성
    bands = []
    for detail in band_details:
        top_track = None
        if detail["top_track"]:
            top_track = TopTrackResponse(
                title=detail["top_track"]["title"],
                externalUrl=detail["top_track"]["externalUrl"],
            )
        
        bands.append(RecommendedBandFinal(
            bandId=detail["band_id"],
            score=round(detail["score"], 4) if detail["score"] else 0.0,
            bandName=detail["band_name"],
            imageUrl=detail["image_url"],
            topTrack=top_track,
            keywords=detail["keywords"],
        ))
    
    logger.info(f"[최종 추천 API] 응답 완료 - {len(bands)}개 밴드 반환")
    
    return FinalRecommendationResponse(
        statusCode=200,
        isSuccess=True,
        message="추천 밴드 업데이트 API",
        payload=RecommendationPayload(bands=bands),
    )
