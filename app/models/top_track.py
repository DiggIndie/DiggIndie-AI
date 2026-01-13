# app/models/top_track.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class TopTrack(Base):
    """top_track 테이블 매핑 - 밴드의 대표곡"""
    __tablename__ = "top_track"

    id = Column("top_track_id", Integer, primary_key=True, index=True)
    band_id = Column(Integer, ForeignKey("band.band_id"), nullable=False, unique=True, index=True)
    title = Column(String(200), nullable=False)
    external_url = Column("external_url", String(300), nullable=False)

    # Relationship
    band = relationship("Band", backref="top_track", uselist=False)
