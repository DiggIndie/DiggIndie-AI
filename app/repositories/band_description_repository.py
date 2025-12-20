from typing import List, Tuple, Set

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.band_description import BandDescription


def get_band_description(db: Session, band_id: int) -> BandDescription | None:
    return (
        db.query(BandDescription)
        .filter(BandDescription.band_id == band_id)
        .first()
    )


def get_band_descriptions_by_ids(db: Session, band_ids: List[int]) -> List[BandDescription]:
    """여러 band_id로 BandDescription 조회 (embedding 있는 것만)"""
    return (
        db.query(BandDescription)
        .filter(
            BandDescription.band_id.in_(band_ids),
            BandDescription.embedding.isnot(None),
        )
        .all()
    )


def get_all_band_descriptions_with_embedding(db: Session) -> List[BandDescription]:
    """embedding이 있는 모든 BandDescription 조회"""
    return (
        db.query(BandDescription)
        .filter(BandDescription.embedding.isnot(None))
        .all()
    )


def find_similar_bands_by_embedding(
    db: Session,
    user_embedding: List[float],
    top_k: int = 3,
    exclude_band_ids: Set[int] | None = None,
) -> List[Tuple[int, float]]:
    """
    pgvector를 활용하여 DB에서 코사인 유사도 계산 후 상위 k개 반환.
    
    Args:
        db: DB 세션
        user_embedding: 사용자 임베딩 벡터
        top_k: 반환할 밴드 수
        exclude_band_ids: 제외할 band_id 집합
    
    Returns:
        [(band_id, score), ...] 형태의 리스트 (유사도 높은 순)
    """
    exclude_band_ids = exclude_band_ids or set()
    
    # pgvector의 <=> 연산자는 코사인 거리를 반환 (0~2 범위)
    # 코사인 유사도 = 1 - 코사인 거리
    query = text("""
        SELECT band_id, 1 - (embedding <=> :vec) AS score
        FROM band_description
        WHERE embedding IS NOT NULL
          AND (:no_exclude OR band_id != ALL(:exclude_ids))
        ORDER BY embedding <=> :vec
        LIMIT :k
    """)
    
    # PostgreSQL 배열 형식으로 변환
    embedding_str = "[" + ",".join(map(str, user_embedding)) + "]"
    exclude_list = list(exclude_band_ids) if exclude_band_ids else []
    
    result = db.execute(
        query,
        {
            "vec": embedding_str,
            "k": top_k,
            "no_exclude": len(exclude_list) == 0,
            "exclude_ids": exclude_list,
        }
    )
    
    return [(row.band_id, float(row.score)) for row in result]
