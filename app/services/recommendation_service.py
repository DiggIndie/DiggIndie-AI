from typing import List, Tuple, Dict, Any
import logging

import numpy as np
from sklearn.cluster import KMeans
from sqlalchemy.orm import Session

from app.repositories.band_description_repository import (
    get_band_descriptions_by_ids,
    find_similar_bands_by_embedding,
    get_bands_with_keywords_by_ids,
    get_keywords_by_ids,
)
from app.services.embedding_service import embedding_service

# 로거 설정
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def embed_keywords(keywords: List[str]) -> np.ndarray:
    """
    키워드 리스트를 문장으로 합쳐서 임베딩 벡터 생성.
    
    Args:
        keywords: 키워드 텍스트 리스트
    
    Returns:
        키워드 임베딩 벡터 (1536차원)
    """
    if not keywords:
        raise ValueError("키워드 리스트가 비어있습니다.")
    
    # 키워드를 공백으로 연결하여 문장 생성
    keyword_sentence = " ".join(keywords)
    
    logger.info("-" * 50)
    logger.info("[키워드 임베딩 생성]")
    logger.info(f"  입력 키워드 개수: {len(keywords)}")
    logger.info(f"  키워드 목록: {keywords}")
    logger.info(f"  결합 문장: \"{keyword_sentence}\"")
    
    model_name, embedding = embedding_service.embed_single_text(keyword_sentence)
    
    embedding_array = np.array(embedding)
    
    logger.info(f"  임베딩 모델: {model_name}")
    logger.info(f"  벡터 차원: {len(embedding)}")
    logger.info(f"  벡터 norm: {np.linalg.norm(embedding_array):.4f}")
    logger.info(f"  벡터 샘플 (첫 5개): {embedding_array[:5]}")
    logger.info("-" * 50)
    
    return embedding_array


def slerp(v0: np.ndarray, v1: np.ndarray, t: float) -> np.ndarray:
    """
    Spherical Linear Interpolation (구면 선형 보간).
    
    두 벡터를 구면 위에서 t 비율만큼 보간합니다.
    t=0이면 v0, t=1이면 v1, t=0.2이면 v0에서 v1 방향으로 20% 이동.
    
    Args:
        v0: 시작 벡터 (사용자 벡터)
        v1: 끝 벡터 (키워드 벡터)
        t: 보간 비율 (0~1)
    
    Returns:
        보간된 벡터
    """
    logger.info("-" * 50)
    logger.info("[Slerp 구면 선형 보간]")
    
    # 원본 벡터 정보
    v0_original_norm = np.linalg.norm(v0)
    v1_original_norm = np.linalg.norm(v1)
    logger.info(f"  사용자 벡터 원본 norm: {v0_original_norm:.4f}")
    logger.info(f"  키워드 벡터 원본 norm: {v1_original_norm:.4f}")
    
    # 정규화
    v0_norm = v0 / v0_original_norm
    v1_norm = v1 / v1_original_norm
    
    # 두 벡터 사이의 각도 계산
    dot = np.clip(np.dot(v0_norm, v1_norm), -1.0, 1.0)
    theta = np.arccos(dot)
    theta_degrees = np.degrees(theta)
    
    logger.info(f"  두 벡터 간 코사인 유사도: {dot:.4f}")
    logger.info(f"  두 벡터 간 각도 (θ): {theta_degrees:.2f}°")
    logger.info(f"  보간 비율 (t): {t:.3f} ({t*100:.1f}%)")
    
    # 각도가 매우 작으면 (거의 같은 방향) 선형 보간
    if theta < 1e-6:
        logger.info("  ⚠️ 두 벡터가 거의 동일한 방향 → 사용자 벡터 유지")
        logger.info("-" * 50)
        return v0_norm
    
    # Slerp 공식
    sin_theta = np.sin(theta)
    result = (np.sin((1 - t) * theta) / sin_theta) * v0_norm + \
             (np.sin(t * theta) / sin_theta) * v1_norm
    
    # 결과 분석
    rotation_angle = theta_degrees * t
    logger.info(f"  실제 회전 각도: {rotation_angle:.2f}° (θ × t)")
    
    # 회전 후 벡터와 원본들 간의 유사도
    result_v0_sim = np.dot(result, v0_norm)
    result_v1_sim = np.dot(result, v1_norm)
    logger.info(f"  [회전 후 벡터] ↔ [원본 사용자 벡터] 유사도: {result_v0_sim:.4f}")
    logger.info(f"  [회전 후 벡터] ↔ [키워드 벡터] 유사도: {result_v1_sim:.4f}")
    logger.info(f"  회전 후 벡터 norm: {np.linalg.norm(result):.4f}")
    logger.info("-" * 50)
    
    return result


def adaptive_t(
    user_emb: np.ndarray,
    keyword_emb: np.ndarray,
    base_t: float = 0.25,
) -> float:
    """
    유사도 기반으로 보간 비율 t를 동적으로 계산.
    
    - 유사도 높음 (이미 비슷함) → t 작게 (적게 틀기)
    - 유사도 낮음 (많이 다름) → t 크게 (더 틀기)
    
    Args:
        user_emb: 사용자 임베딩 벡터
        keyword_emb: 키워드 임베딩 벡터
        base_t: 기본 보간 비율
    
    Returns:
        조정된 t 값 (0.05 ~ 0.4 범위)
    """
    logger.info("-" * 50)
    logger.info("[Adaptive t 계산 - 유사도 기반 키워드 영향력 조절]")
    
    # 코사인 유사도 계산
    user_norm = np.linalg.norm(user_emb)
    keyword_norm = np.linalg.norm(keyword_emb)
    dot_product = np.dot(user_emb, keyword_emb)
    similarity = dot_product / (user_norm * keyword_norm)
    
    logger.info(f"  사용자 벡터 norm: {user_norm:.4f}")
    logger.info(f"  키워드 벡터 norm: {keyword_norm:.4f}")
    logger.info(f"  내적 (dot product): {dot_product:.4f}")
    logger.info(f"  코사인 유사도: {similarity:.4f}")
    
    # 유사도에 따라 t 조정
    # 공식: t = base_t × (1.2 - similarity × 0.5)
    raw_t = base_t * (1.2 - similarity * 0.5)
    
    logger.info(f"  기본 t (base_t): {base_t:.3f}")
    logger.info(f"  조정 공식: t = {base_t} × (1.2 - {similarity:.4f} × 0.5)")
    logger.info(f"  계산된 t (raw): {raw_t:.4f}")
    
    # 범위 제한
    final_t = float(np.clip(raw_t, 0.05, 0.4))
    
    if raw_t != final_t:
        logger.info(f"  ⚠️ 범위 클리핑: {raw_t:.4f} → {final_t:.3f} (범위: 0.05~0.40)")
    
    # 해석
    if similarity >= 0.8:
        interpretation = "높음 (이미 비슷함) → 키워드 영향 최소화"
    elif similarity >= 0.5:
        interpretation = "중간 → 키워드 적당히 반영"
    else:
        interpretation = "낮음 (방향 다름) → 키워드 영향 극대화"
    
    logger.info(f"  유사도 해석: {interpretation}")
    logger.info(f"  ✅ 최종 t: {final_t:.3f} ({final_t*100:.1f}% 키워드 방향으로 회전)")
    logger.info("-" * 50)
    
    return final_t


def build_user_embedding(embeddings: List[np.ndarray]) -> np.ndarray:
    """
    사용자가 선택한 밴드들의 임베딩으로 사용자 임베딩 벡터 생성.
    - 1개: 그대로 사용
    - 2개: 단순 평균
    - 3개 이상: k=3 K-means 클러스터링 후 멤버 수 기반 가중 평균
    """
    n = len(embeddings)
    logger.info(f"[build_user_embedding] 입력 임베딩 개수: {n}")
    
    if n == 1:
        logger.info("[build_user_embedding] 1개 → 그대로 사용")
        return embeddings[0]
    
    if n == 2:
        logger.info("[build_user_embedding] 2개 → 단순 평균")
        return np.mean(embeddings, axis=0)
    
    # 3개 이상: K-means (k=3)
    logger.info("[build_user_embedding] 3개 이상 → K-means(k=3) 클러스터링 시작")
    
    X = np.array(embeddings)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    
    # 각 클러스터의 centroid와 멤버 수 계산
    centroids = kmeans.cluster_centers_  # shape: (3, dim)
    cluster_counts = np.bincount(labels, minlength=3)  # 각 클러스터의 멤버 수
    
    # 클러스터링 결과 로그
    logger.info("=" * 50)
    logger.info("[클러스터링 결과]")
    for i in range(3):
        logger.info(f" 클러스터 {i}: {cluster_counts[i]}개 벡터")
        logger.info(f" centroid: {centroids[i][:10]}")
    logger.info("=" * 70)
    
    # 가중 평균 (멤버 수 기반)
    total = cluster_counts.sum()
    weights = cluster_counts / total  # shape: (3,)
    
    logger.info(f"[가중치] 클러스터별 가중치: {weights}")
    
    user_embedding = np.average(centroids, axis=0, weights=weights)
    
    logger.info(f"[사용자 벡터] 최종 사용자 임베딩 : {user_embedding[:10]}")
    logger.info(f"[사용자 벡터] 벡터 norm: {np.linalg.norm(user_embedding):.4f}")
    
    return user_embedding


def recommend_bands_v1(
    db: Session,
    band_ids: List[int],
    top_k: int = 3,
    exclude_input: bool = True,
) -> List[Dict[str, Any]]:
    """
    [V1] 밴드 기반 추천.
    
    사용자가 선택한 밴드 ID 목록을 기반으로 추천 밴드 반환.
    
    Args:
        db: DB 세션
        band_ids: 사용자가 선택한 밴드 ID 리스트
        top_k: 반환할 추천 밴드 수
        exclude_input: 입력한 밴드를 추천 결과에서 제외할지 여부
    
    Returns:
        [{"band_id": int, "score": float, "band_name": str, "image_url": str, "band_music": str, "keywords": [str]}, ...]
    """
    logger.info("=" * 70)
    logger.info("🎸 [V1] 밴드 기반 추천 시작")
    logger.info("=" * 70)
    logger.info(f"[V1 입력]")
    logger.info(f"  밴드 IDs: {band_ids}")
    logger.info(f"  요청 개수: {len(band_ids)}개")
    logger.info(f"  반환할 추천 수 (top_k): {top_k}")
    logger.info(f"  입력 밴드 제외 여부: {exclude_input}")
    
    unique_band_ids = list(dict.fromkeys(band_ids))
    if len(unique_band_ids) != len(band_ids):
        logger.info(f"  ⚠️ 중복 제거: {len(band_ids)}개 → {len(unique_band_ids)}개")
    
    # 1. 사용자가 선택한 밴드들의 임베딩 가져오기
    logger.info("-" * 50)
    logger.info("[V1 Step 1] 밴드 임베딩 조회")
    selected_bands = get_band_descriptions_by_ids(db, unique_band_ids)
    
    if not selected_bands:
        raise ValueError("선택한 밴드 중 임베딩이 있는 밴드가 없습니다.")
    
    logger.info(f"  조회된 밴드: {len(selected_bands)}개")
    for band in selected_bands:
        emb_norm = np.linalg.norm(np.array(band.embedding)) if band.embedding is not None else 0
        logger.info(f"    - band_id={band.band_id}, 임베딩 norm={emb_norm:.4f}")
    
    selected_embeddings = [np.array(b.embedding) for b in selected_bands]
    selected_band_ids = {b.band_id for b in selected_bands}
    
    # 2. 사용자 임베딩 벡터 생성
    logger.info("-" * 50)
    logger.info("[V1 Step 2] 사용자 벡터 생성")
    user_embedding = build_user_embedding(selected_embeddings)
    logger.info(f"  최종 사용자 벡터 norm: {np.linalg.norm(user_embedding):.4f}")
    
    # 3. DB 쿼리로 코사인 유사도 계산 + 정렬 + top_k 반환 (pgvector 활용)
    exclude_ids = selected_band_ids if exclude_input else None
    
    logger.info("-" * 50)
    logger.info("[V1 Step 3] pgvector 유사도 검색")
    logger.info(f"  제외할 밴드: {len(exclude_ids) if exclude_ids else 0}개 {list(exclude_ids) if exclude_ids else []}")
    
    similarity_results = find_similar_bands_by_embedding(
        db=db,
        user_embedding=user_embedding.tolist(),
        top_k=top_k,
        exclude_band_ids=exclude_ids,
    )
    
    # 결과 로그
    logger.info("=" * 70)
    logger.info(f"[V1 추천 결과] 상위 {top_k}개:")
    for i, (band_id, score) in enumerate(similarity_results[:top_k], 1):
        logger.info(f"  {i}. band_id={band_id}, score={score:.4f}")
    logger.info("=" * 70)
    
    # 4. 추천된 밴드들의 상세 정보 조회
    recommended_band_ids = [band_id for band_id, _ in similarity_results[:top_k]]
    bands_info = get_bands_with_keywords_by_ids(db, recommended_band_ids)
    
    # 5. 결과 조합
    results = []
    for band_id, score in similarity_results[:top_k]:
        band_info = bands_info.get(band_id, {})
        results.append({
            "band_id": band_id,
            "score": score,
            "band_name": band_info.get("band_name"),
            "image_url": band_info.get("main_image"),
            "band_music": band_info.get("main_music"),
            "keywords": band_info.get("keywords", []),
        })
    
    logger.info(f"[V1 최종 결과] 밴드 상세 정보 포함 {len(results)}개 반환")
    
    return results


def recommend_bands_v2(
    db: Session,
    band_ids: List[int],
    keyword_ids: List[int],
    top_k: int = 3,
    exclude_input: bool = True,
) -> List[Dict[str, Any]]:
    """
    [V2] 밴드 + 키워드 기반 추천.
    
    키워드 임베딩을 Slerp로 사용자 벡터에 반영합니다.
    유사도 기반으로 키워드 영향력이 동적으로 조절됩니다.
    
    Args:
        db: DB 세션
        band_ids: 사용자가 선택한 밴드 ID 리스트
        keyword_ids: 사용자가 선택한 키워드 ID 리스트
        top_k: 반환할 추천 밴드 수
        exclude_input: 입력한 밴드를 추천 결과에서 제외할지 여부
    
    Returns:
        [{"band_id": int, "score": float, ...}, ...]
    """
    logger.info("=" * 70)
    logger.info("🎸🏷️ [V2] 밴드 + 키워드 기반 추천 시작")
    logger.info("=" * 70)
    logger.info("[V2 입력]")
    logger.info(f"  밴드 IDs: {band_ids}")
    logger.info(f"  밴드 개수: {len(band_ids)}개")
    logger.info(f"  키워드 IDs: {keyword_ids}")
    logger.info(f"  키워드 개수: {len(keyword_ids)}개")
    logger.info(f"  반환할 추천 수 (top_k): {top_k}")
    logger.info(f"  입력 밴드 제외 여부: {exclude_input}")
    
    unique_band_ids = list(dict.fromkeys(band_ids))
    if len(unique_band_ids) != len(band_ids):
        logger.info(f"  ⚠️ 밴드 중복 제거: {len(band_ids)}개 → {len(unique_band_ids)}개")
    
    # 1. 사용자가 선택한 밴드들의 임베딩 가져오기
    logger.info("-" * 50)
    logger.info("[V2 Step 1] 밴드 임베딩 조회")
    selected_bands = get_band_descriptions_by_ids(db, unique_band_ids)
    
    if not selected_bands:
        raise ValueError("선택한 밴드 중 임베딩이 있는 밴드가 없습니다.")
    
    logger.info(f"  조회된 밴드: {len(selected_bands)}개")
    for band in selected_bands:
        emb_norm = np.linalg.norm(np.array(band.embedding)) if band.embedding is not None else 0
        logger.info(f"    - band_id={band.band_id}, 임베딩 norm={emb_norm:.4f}")
    
    selected_embeddings = [np.array(b.embedding) for b in selected_bands]
    selected_band_ids = {b.band_id for b in selected_bands}
    
    # 2. 밴드 기반 사용자 임베딩 벡터 생성 (V1과 동일)
    logger.info("-" * 50)
    logger.info("[V2 Step 2] 밴드 기반 사용자 벡터 생성")
    user_embedding_before = build_user_embedding(selected_embeddings)
    user_embedding = user_embedding_before.copy()
    
    user_vec_norm_before = np.linalg.norm(user_embedding_before)
    logger.info(f"  밴드 기반 사용자 벡터 norm: {user_vec_norm_before:.4f}")
    
    # 3. 키워드가 있으면 Slerp로 결합
    logger.info("-" * 50)
    logger.info("[V2 Step 3] 키워드 벡터 생성 및 Slerp 적용")
    
    keyword_applied = False
    if keyword_ids:
        # 키워드 텍스트 조회
        keywords = get_keywords_by_ids(db, keyword_ids)
        
        if keywords:
            logger.info(f"  조회된 키워드: {len(keywords)}개")
            logger.info(f"  키워드 목록: {keywords}")
            
            # 키워드 임베딩 생성
            keyword_embedding = embed_keywords(keywords)
            
            # 유사도 기반 t 계산
            t = adaptive_t(user_embedding, keyword_embedding)
            
            # Slerp로 사용자 벡터에 키워드 방향 반영
            user_embedding = slerp(user_embedding, keyword_embedding, t)
            keyword_applied = True
            
            # 변화량 분석
            logger.info("-" * 50)
            logger.info("[V2 벡터 변화 분석]")
            
            # 변화 전후 비교
            change_magnitude = np.linalg.norm(user_embedding - user_embedding_before / user_vec_norm_before)
            before_after_similarity = np.dot(
                user_embedding_before / user_vec_norm_before,
                user_embedding / np.linalg.norm(user_embedding)
            )
            
            logger.info(f"  원본 사용자 벡터 norm: {user_vec_norm_before:.4f}")
            logger.info(f"  회전 후 벡터 norm: {np.linalg.norm(user_embedding):.4f}")
            logger.info(f"  [원본 사용자 벡터] ↔ [회전 후 벡터] 유사도: {before_after_similarity:.4f}")
            logger.info(f"  키워드 기여도 (t): {t:.3f} ({t*100:.1f}%)")
            logger.info(f"  ✅ 키워드 반영 완료!")
        else:
            logger.info("  ⚠️ 유효한 키워드 없음 → 밴드 기반 벡터만 사용")
    else:
        logger.info("  ⚠️ 키워드 없음 → 밴드 기반 벡터만 사용")
    
    # 4. DB 쿼리로 코사인 유사도 계산
    exclude_ids = selected_band_ids if exclude_input else None
    
    logger.info("-" * 50)
    logger.info("[V2 Step 4] pgvector 유사도 검색")
    logger.info(f"  최종 사용자 벡터 norm: {np.linalg.norm(user_embedding):.4f}")
    logger.info(f"  키워드 적용 여부: {'✅ 적용됨' if keyword_applied else '❌ 미적용'}")
    logger.info(f"  제외할 밴드: {len(exclude_ids) if exclude_ids else 0}개 {list(exclude_ids) if exclude_ids else []}")
    
    similarity_results = find_similar_bands_by_embedding(
        db=db,
        user_embedding=user_embedding.tolist(),
        top_k=top_k,
        exclude_band_ids=exclude_ids,
    )
    
    # 결과 로그
    logger.info("=" * 70)
    logger.info(f"[V2 추천 결과] 상위 {top_k}개:")
    for i, (band_id, score) in enumerate(similarity_results[:top_k], 1):
        logger.info(f"  {i}. band_id={band_id}, score={score:.4f}")
    logger.info("=" * 70)
    
    # 5. 추천된 밴드들의 상세 정보 조회
    recommended_band_ids = [band_id for band_id, _ in similarity_results[:top_k]]
    bands_info = get_bands_with_keywords_by_ids(db, recommended_band_ids)
    
    # 6. 결과 조합
    results = []
    for band_id, score in similarity_results[:top_k]:
        band_info = bands_info.get(band_id, {})
        results.append({
            "band_id": band_id,
            "score": score,
            "band_name": band_info.get("band_name"),
            "image_url": band_info.get("main_image"),
            "band_music": band_info.get("main_music"),
            "keywords": band_info.get("keywords", []),
        })
    
    logger.info(f"[V2 최종 결과] 밴드 상세 정보 포함 {len(results)}개 반환")
    
    return results


def recommend_bands_v3(
    db: Session,
    band_ids: List[int],
    keyword_ids: List[int],
    exclude_input: bool = True,
) -> List[Dict[str, Any]]:
    """
    [V3] 클러스터별 키워드 반영 추천 (5개 반환).
    
    각 클러스터의 centroid에 키워드 벡터를 Slerp로 적용하여
    3개의 조정된 중심 벡터를 만들고, 각각에 가장 가까운 밴드 2개씩 검색.
    
    - 각 클러스터의 1등 3개: 필수 반환
    - 각 클러스터의 2등 중 점수 높은 2개: 추가 반환
    - 총 5개 밴드 반환
    
    밴드가 3개 미만이면 V2로 폴백.
    
    Args:
        db: DB 세션
        band_ids: 사용자가 선택한 밴드 ID 리스트
        keyword_ids: 사용자가 선택한 키워드 ID 리스트
        exclude_input: 입력한 밴드를 추천 결과에서 제외할지 여부
    
    Returns:
        [{"band_id": int, "score": float, ...}, ...]
    """
    logger.info("=" * 70)
    logger.info("🎸🏷️🎯 [V3] 클러스터별 키워드 반영 추천 시작")
    logger.info("=" * 70)
    logger.info("[V3 입력]")
    logger.info(f"  밴드 IDs: {band_ids}")
    logger.info(f"  밴드 개수: {len(band_ids)}개")
    logger.info(f"  키워드 IDs: {keyword_ids}")
    logger.info(f"  키워드 개수: {len(keyword_ids)}개")
    
    unique_band_ids = list(dict.fromkeys(band_ids))
    
    # 밴드가 3개 미만이면 V2로 폴백
    if len(unique_band_ids) < 3:
        logger.info(f"  ⚠️ 밴드 {len(unique_band_ids)}개 < 3개 → V2로 폴백")
        logger.info("=" * 70)
        return recommend_bands_v2(
            db=db,
            band_ids=band_ids,
            keyword_ids=keyword_ids,
            top_k=3,
            exclude_input=exclude_input,
        )
    
    # 1. 사용자가 선택한 밴드들의 임베딩 가져오기
    logger.info("-" * 50)
    logger.info("[V3 Step 1] 밴드 임베딩 조회")
    selected_bands = get_band_descriptions_by_ids(db, unique_band_ids)
    
    if not selected_bands:
        raise ValueError("선택한 밴드 중 임베딩이 있는 밴드가 없습니다.")
    
    if len(selected_bands) < 3:
        logger.info(f"  ⚠️ 임베딩 있는 밴드 {len(selected_bands)}개 < 3개 → V2로 폴백")
        return recommend_bands_v2(
            db=db,
            band_ids=band_ids,
            keyword_ids=keyword_ids,
            top_k=3,
            exclude_input=exclude_input,
        )
    
    logger.info(f"  조회된 밴드: {len(selected_bands)}개")
    for band in selected_bands:
        emb_norm = np.linalg.norm(np.array(band.embedding)) if band.embedding is not None else 0
        logger.info(f"    - band_id={band.band_id}, 임베딩 norm={emb_norm:.4f}")
    
    selected_embeddings = [np.array(b.embedding) for b in selected_bands]
    selected_band_ids = {b.band_id for b in selected_bands}
    
    # 2. K-means 클러스터링 (k=3)
    logger.info("-" * 50)
    logger.info("[V3 Step 2] K-means 클러스터링 (k=3)")
    
    X = np.array(selected_embeddings)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)
    centroids = kmeans.cluster_centers_  # shape: (3, dim)
    cluster_counts = np.bincount(labels, minlength=3)
    
    logger.info("[클러스터링 결과]")
    for i in range(3):
        logger.info(f"  클러스터 {i}: {cluster_counts[i]}개 벡터, centroid norm={np.linalg.norm(centroids[i]):.4f}")
    
    # 3. 키워드 임베딩 생성
    logger.info("-" * 50)
    logger.info("[V3 Step 3] 키워드 임베딩 생성")
    
    keyword_embedding = None
    if keyword_ids:
        keywords = get_keywords_by_ids(db, keyword_ids)
        if keywords:
            logger.info(f"  조회된 키워드: {keywords}")
            keyword_embedding = embed_keywords(keywords)
        else:
            logger.info("  ⚠️ 유효한 키워드 없음")
    else:
        logger.info("  ⚠️ 키워드 없음")
    
    # 4. 각 centroid에 Slerp 적용
    logger.info("-" * 50)
    logger.info("[V3 Step 4] 각 클러스터 centroid에 키워드 Slerp 적용")
    
    adjusted_centroids = []
    for i in range(3):
        centroid = centroids[i]
        
        if keyword_embedding is not None and cluster_counts[i] > 0:
            # 유사도 기반 t 계산
            t = adaptive_t(centroid, keyword_embedding)
            logger.info(f"  클러스터 {i}: t={t:.3f}")
            
            # Slerp로 키워드 방향 반영
            adjusted = slerp(centroid, keyword_embedding, t)
            adjusted_centroids.append(adjusted)
            
            logger.info(f"    [원본 centroid] ↔ [회전 후 centroid] 유사도: {np.dot(centroid/np.linalg.norm(centroid), adjusted):.4f}")
        else:
            # 키워드 없으면 원본 centroid 사용 (정규화)
            adjusted_centroids.append(centroid / np.linalg.norm(centroid))
            logger.info(f"  클러스터 {i}: 키워드 없음 → 원본 centroid 사용")
    
    # 5. 각 조정된 centroid에 가장 가까운 밴드 2개씩 검색
    logger.info("-" * 50)
    logger.info("[V3 Step 5] 각 클러스터별 상위 2개 밴드 검색")
    
    exclude_ids = selected_band_ids if exclude_input else set()
    cluster_top1 = []  # 각 클러스터의 1등 (band_id, score, cluster_idx)
    cluster_top2 = []  # 각 클러스터의 2등 (band_id, score, cluster_idx)
    already_recommended = set()  # 중복 방지
    
    for i, adj_centroid in enumerate(adjusted_centroids):
        # 빈 클러스터는 스킵
        if cluster_counts[i] == 0:
            logger.info(f"  클러스터 {i}: 비어있음 → 스킵")
            continue
        
        # 해당 centroid로 가장 유사한 밴드 검색 (top_k를 넉넉히 가져와서 중복 체크)
        results = find_similar_bands_by_embedding(
            db=db,
            user_embedding=adj_centroid.tolist(),
            top_k=10,  # 넉넉히 가져옴
            exclude_band_ids=exclude_ids,
        )
        
        # 각 클러스터에서 2개씩 뽑기
        cluster_bands = []
        for band_id, score in results:
            if band_id not in already_recommended:
                cluster_bands.append((band_id, score, i))
                already_recommended.add(band_id)
                if len(cluster_bands) == 2:
                    break
        
        # 1등과 2등 분리
        if len(cluster_bands) >= 1:
            cluster_top1.append(cluster_bands[0])
            logger.info(f"  클러스터 {i} - 1등: band_id={cluster_bands[0][0]}, score={cluster_bands[0][1]:.4f}")
        
        if len(cluster_bands) >= 2:
            cluster_top2.append(cluster_bands[1])
            logger.info(f"  클러스터 {i} - 2등: band_id={cluster_bands[1][0]}, score={cluster_bands[1][1]:.4f}")
        
        if len(cluster_bands) == 0:
            logger.info(f"  클러스터 {i}: 추천할 밴드 없음")
        elif len(cluster_bands) == 1:
            logger.info(f"  클러스터 {i}: 2등 밴드 없음 (1개만 발견)")
    
    # 6. 최종 추천 목록 구성
    logger.info("-" * 50)
    logger.info("[V3 Step 6] 최종 추천 목록 구성")
    
    # 각 클러스터 1등 3개는 필수 포함
    final_recommended = cluster_top1.copy()
    logger.info(f"  필수 포함 (각 클러스터 1등): {len(cluster_top1)}개")
    
    # 각 클러스터 2등 중 점수 높은 순으로 정렬하여 상위 2개 추가
    cluster_top2_sorted = sorted(cluster_top2, key=lambda x: x[1], reverse=True)
    additional_bands = cluster_top2_sorted[:2]
    final_recommended.extend(additional_bands)
    
    logger.info(f"  추가 포함 (2등 중 상위): {len(additional_bands)}개")
    for band_id, score, cluster_idx in additional_bands:
        logger.info(f"    클러스터 {cluster_idx} - band_id={band_id}, score={score:.4f}")
    
    # 7. 최종 점수 순으로 정렬
    final_recommended.sort(key=lambda x: x[1], reverse=True)
    
    logger.info("-" * 50)
    logger.info("[V3 추천 결과] 총 5개 밴드")
    for i, (band_id, score, cluster_idx) in enumerate(final_recommended, 1):
        logger.info(f"  {i}. band_id={band_id}, score={score:.4f} (클러스터 {cluster_idx})")
    
    # 8. 밴드 상세 정보 조회
    recommended_band_ids = [band_id for band_id, _, _ in final_recommended]
    bands_info = get_bands_with_keywords_by_ids(db, recommended_band_ids)
    
    # 9. 결과 조합
    results = []
    for band_id, score, cluster_idx in final_recommended:
        band_info = bands_info.get(band_id, {})
        results.append({
            "band_id": band_id,
            "score": score,
            "band_name": band_info.get("band_name"),
            "image_url": band_info.get("main_image"),
            "band_music": band_info.get("main_music"),
            "keywords": band_info.get("keywords", []),
        })
    
    logger.info("=" * 70)
    logger.info(f"[V3 최종 결과] {len(results)}개 밴드 반환")
    logger.info(f"  - 각 클러스터 1등: 3개 (필수)")
    logger.info(f"  - 각 클러스터 2등 중 상위: 2개 (추가)")
    logger.info("=" * 70)
    
    return results
