from typing import List, Tuple
import logging

import numpy as np
from sklearn.cluster import KMeans
from sqlalchemy.orm import Session

from app.repositories.band_description_repository import (
    get_band_descriptions_by_ids,
    find_similar_bands_by_embedding,
)

# 로거 설정
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


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


def recommend_bands(
    db: Session,
    band_ids: List[int],
    top_k: int = 3,
    exclude_input: bool = True,
) -> List[Tuple[int, float]]:
    """
    사용자가 선택한 밴드 ID 목록을 기반으로 추천 밴드 반환.
    
    Args:
        db: DB 세션
        band_ids: 사용자가 선택한 밴드 ID 리스트
        top_k: 반환할 추천 밴드 수
        exclude_input: 입력한 밴드를 추천 결과에서 제외할지 여부
    
    Returns:
        [(band_id, score), ...] 형태의 리스트 (유사도 높은 순)
    """
    logger.info("=" * 70)
    logger.info(f"[recommend_bands] 요청 밴드 IDs (원본): {band_ids}")
    logger.info("=" * 70)
    
    unique_band_ids = list(dict.fromkeys(band_ids))
    if len(unique_band_ids) != len(band_ids):
        logger.info(f"[중복 제거] {len(band_ids)}개 → {len(unique_band_ids)}개")
    
    # 1. 사용자가 선택한 밴드들의 임베딩 가져오기
    selected_bands = get_band_descriptions_by_ids(db, unique_band_ids)
    
    if not selected_bands:
        raise ValueError("선택한 밴드 중 임베딩이 있는 밴드가 없습니다.")
    
    logger.info(f"[DB 조회] 임베딩 있는 밴드 {len(selected_bands)}개 조회됨")
    
    selected_embeddings = [np.array(b.embedding) for b in selected_bands]
    selected_band_ids = {b.band_id for b in selected_bands}
    
    # 2. 사용자 임베딩 벡터 생성
    user_embedding = build_user_embedding(selected_embeddings)
    
    # 3. DB 쿼리로 코사인 유사도 계산 + 정렬 + top_k 반환 (pgvector 활용)
    exclude_ids = selected_band_ids if exclude_input else None
    
    logger.info(f"[DB 쿼리] pgvector로 코사인 유사도 계산 중... (제외 밴드: {len(exclude_ids) if exclude_ids else 0}개)")
    
    results = find_similar_bands_by_embedding(
        db=db,
        user_embedding=user_embedding.tolist(),
        top_k=top_k,
        exclude_band_ids=exclude_ids,
    )
    
    # 결과 로그
    logger.info("=" * 70)
    logger.info(f"[추천 결과] 상위 {top_k}개:")
    for i, (band_id, score) in enumerate(results[:top_k], 1):
        logger.info(f"  {i}. band_id={band_id}, score={score:.4f}")
    logger.info("=" * 70)
    
    return results[:top_k]
