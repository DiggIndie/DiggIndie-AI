from sqlalchemy.orm import Session

from app.models.band_description import BandDescription


def get_band_description(db: Session, band_id: int) -> BandDescription | None:
    return (
        db.query(BandDescription)
        .filter(BandDescription.band_id == band_id)
        .first()
    )
