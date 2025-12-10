# app/api/v1/band_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.schemas.band_description_schemas import BandDescriptionResponse
from app.services.band_description_service import fetch_band_description

router = APIRouter(
    prefix="/bands",
    tags=["bands"],
)


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
