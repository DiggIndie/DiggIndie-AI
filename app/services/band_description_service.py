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
        embedding_list = list(row.embedding)

    return BandDescriptionResponse(
        bandId=row.band_id,
        description=row.description,
        createdAt=row.created_at,
        updatedAt=row.updated_at,
        deletedAt=row.deleted_at,
        embedding=embedding_list,
    )
