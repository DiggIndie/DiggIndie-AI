from typing import List, Tuple, Set, Dict, Any, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.band_description import BandDescription
from app.models.member import Member
from app.models.member_band import MemberBand
from app.models.member_keyword import MemberKeyword
from app.models.band_recommend import BandRecommend


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


# ============================================================
# Member 관련 함수
# ============================================================

def get_member_by_external_id(db: Session, external_id: str) -> Optional[Member]:
    """
    externalId로 Member 조회.
    
    Args:
        db: DB 세션
        external_id: JWT에서 추출한 externalId (UUID)
    
    Returns:
        Member 객체 또는 None
    """
    return (
        db.query(Member)
        .filter(
            Member.external_id == external_id,
            Member.deleted_at.is_(None)
        )
        .first()
    )


def get_member_band_ids(db: Session, member_id: int) -> List[int]:
    """
    사용자가 선택한 밴드 ID 목록 조회.
    
    Args:
        db: DB 세션
        member_id: 회원 ID
    
    Returns:
        band_id 리스트
    """
    query = text("""
        SELECT band_id
        FROM member_band
        WHERE member_id = :member_id
          AND band_id IS NOT NULL
          AND deleted_at IS NULL
    """)
    
    result = db.execute(query, {"member_id": member_id})
    return [row.band_id for row in result]


def get_member_keyword_ids(db: Session, member_id: int) -> List[int]:
    """
    사용자가 선택한 키워드 ID 목록 조회.
    
    Args:
        db: DB 세션
        member_id: 회원 ID
    
    Returns:
        keyword_id 리스트
    """
    query = text("""
        SELECT keyword_id
        FROM member_keyword
        WHERE member_id = :member_id
          AND deleted_at IS NULL
    """)
    
    result = db.execute(query, {"member_id": member_id})
    return [row.keyword_id for row in result]


# ============================================================
# BandRecommend 관련 함수
# ============================================================

def delete_band_recommends(db: Session, member_id: int) -> int:
    """
    사용자의 기존 추천 밴드를 모두 삭제 (soft delete 아닌 hard delete).
    
    Args:
        db: DB 세션
        member_id: 회원 ID
    
    Returns:
        삭제된 레코드 수
    """
    deleted_count = (
        db.query(BandRecommend)
        .filter(BandRecommend.member_id == member_id)
        .delete(synchronize_session=False)
    )
    return deleted_count


def save_band_recommends(
    db: Session,
    member_id: int,
    recommendations: List[Dict[str, Any]],
) -> List[BandRecommend]:
    """
    추천 밴드를 저장. score가 높은 순으로 priority 1, 2, 3 부여.
    
    Args:
        db: DB 세션
        member_id: 회원 ID
        recommendations: [{"band_id": int, "score": float}, ...] 형태
    
    Returns:
        저장된 BandRecommend 객체 리스트
    """
    # score 높은 순으로 정렬
    sorted_recs = sorted(recommendations, key=lambda x: x["score"], reverse=True)
    
    saved_recommends = []
    now = datetime.now()
    
    for priority, rec in enumerate(sorted_recs, start=1):
        band_recommend = BandRecommend(
            priority=priority,
            score=rec["score"],
            member_id=member_id,
            band_id=rec["band_id"],
        )
        band_recommend.created_at = now
        band_recommend.updated_at = now
        db.add(band_recommend)
        saved_recommends.append(band_recommend)
    
    db.flush()  # ID 생성을 위해 flush
    return saved_recommends


def get_band_recommends_with_details(
    db: Session,
    member_id: int,
) -> List[Dict[str, Any]]:
    """
    사용자의 추천 밴드를 Band, TopTrack, Keyword 정보와 함께 조회.
    
    Args:
        db: DB 세션
        member_id: 회원 ID
    
    Returns:
        [{
            "band_id": int,
            "band_name": str,
            "image_url": str,
            "top_track": {"title": str, "external_url": str} or None,
            "keywords": [str, ...]
        }, ...]
    """
    # 추천 밴드 조회 (priority 순)
    query = text("""
        SELECT br.band_id, br.priority, br.score,
               b.band_name, b.main_image,
               tt.title as track_title, tt.external_url as track_url
        FROM band_recommend br
        JOIN band b ON br.band_id = b.band_id
        LEFT JOIN top_track tt ON b.band_id = tt.band_id
        WHERE br.member_id = :member_id
          AND b.deleted_at IS NULL
        ORDER BY br.priority ASC
    """)
    
    result = db.execute(query, {"member_id": member_id})
    
    bands_data = []
    band_ids = []
    
    for row in result:
        band_ids.append(row.band_id)
        
        top_track = None
        if row.track_title:
            top_track = {
                "title": row.track_title,
                "externalUrl": row.track_url,
            }
        
        bands_data.append({
            "band_id": row.band_id,
            "score": row.score,
            "band_name": row.band_name,
            "image_url": row.main_image,
            "top_track": top_track,
            "keywords": [],  # 나중에 채움
        })
    
    # 키워드 조회
    if band_ids:
        keyword_query = text("""
            SELECT bk.band_id, k.keyword
            FROM band_keyword bk
            JOIN keyword k ON bk.keyword_id = k.keyword_id
            WHERE bk.band_id = ANY(:band_ids)
              AND bk.deleted_at IS NULL
              AND k.deleted_at IS NULL
        """)
        
        keyword_result = db.execute(keyword_query, {"band_ids": band_ids})
        
        # band_id -> keywords 매핑
        band_keywords: Dict[int, List[str]] = {bid: [] for bid in band_ids}
        for row in keyword_result:
            if row.keyword:
                band_keywords[row.band_id].append(row.keyword)
        
        # 키워드 채우기
        for band_data in bands_data:
            band_data["keywords"] = band_keywords.get(band_data["band_id"], [])
    
    return bands_data
