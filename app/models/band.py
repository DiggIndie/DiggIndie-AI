# app/models/band.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship

from app.core.db import Base


class Band(Base):
    """band 테이블 매핑"""
    __tablename__ = "band"

    id = Column("band_id", Integer, primary_key=True, index=True)
    band_name = Column(String(20), nullable=True)
    main_image = Column(String(200), nullable=True)
    main_url = Column(String(200), nullable=True)
    main_music = Column(String(200), nullable=True)
    description = Column(Text, nullable=False)
    spotify_id = Column(String(100), nullable=True)
    is_band = Column(Boolean, nullable=True, default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relationship with BandKeyword
    band_keywords = relationship("BandKeyword", back_populates="band")
