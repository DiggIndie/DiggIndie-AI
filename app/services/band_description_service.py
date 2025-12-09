# app/services/band_description_service.py
from typing import Optional

from sqlalchemy.orm import Session

from app.schemas.band_description_schemas import BandDescriptionResponse
from app.repositories.band_description_repository import get_band_description


def fetch_band_description(db: Session, band_id: int) -> Optional[BandDescriptionResponse]:
    row = get_band_description(db, band_id)
    if row is None:
        return None

    embedding_list = None
    if row.embedding is not None:
        # pgvector가 list 또는 numpy array를 반환할 수 있으므로 리스트로 변환
        embedding_list = list(row.embedding)

    return BandDescriptionResponse(
        band_id=row.band_id,
        description=row.description,
        created_at=row.created_at,
        updated_at=row.updated_at,
        deleted_at=row.deleted_at,
        embedding=embedding_list,
    )
