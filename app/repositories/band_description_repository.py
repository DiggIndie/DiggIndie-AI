from typing import List, Tuple, Set, Dict, Any

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


def get_bands_with_keywords_by_ids(
    db: Session,
    band_ids: List[int],
) -> Dict[int, Dict[str, Any]]:
    """
    band_id 목록으로 밴드 정보와 키워드를 함께 조회.
    
    Args:
        db: DB 세션
        band_ids: 조회할 band_id 리스트
    
    Returns:
        {band_id: {"band_name": str, "main_image": str, "main_music": str, "keywords": [str, ...]}, ...}
    """
    if not band_ids:
        return {}
    
    # 밴드 기본 정보 조회
    band_query = text("""
        SELECT band_id, band_name, main_image, main_music
        FROM band
        WHERE band_id = ANY(:band_ids)
          AND deleted_at IS NULL
    """)
    
    band_result = db.execute(band_query, {"band_ids": list(band_ids)})
    
    bands_dict: Dict[int, Dict[str, Any]] = {}
    for row in band_result:
        bands_dict[row.band_id] = {
            "band_name": row.band_name,
            "main_image": row.main_image,
            "main_music": row.main_music,
            "keywords": [],
        }
    
    # 키워드 정보 조회 (band_keyword + keyword 조인)
    keyword_query = text("""
        SELECT bk.band_id, k.keyword
        FROM band_keyword bk
        JOIN keyword k ON bk.keyword_id = k.keyword_id
        WHERE bk.band_id = ANY(:band_ids)
          AND bk.deleted_at IS NULL
          AND k.deleted_at IS NULL
    """)
    
    keyword_result = db.execute(keyword_query, {"band_ids": list(band_ids)})
    
    for row in keyword_result:
        if row.band_id in bands_dict:
            bands_dict[row.band_id]["keywords"].append(row.keyword)
    
    return bands_dict


def get_keywords_by_ids(db: Session, keyword_ids: List[int]) -> List[str]:
    """
    keyword_id 목록으로 키워드 텍스트 조회.
    
    Args:
        db: DB 세션
        keyword_ids: 조회할 keyword_id 리스트
    
    Returns:
        키워드 텍스트 리스트
    """
    if not keyword_ids:
        return []
    
    query = text("""
        SELECT keyword
        FROM keyword
        WHERE keyword_id = ANY(:keyword_ids)
          AND deleted_at IS NULL
    """)
    
    result = db.execute(query, {"keyword_ids": list(keyword_ids)})
    
    return [row.keyword for row in result if row.keyword]
