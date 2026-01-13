# app/models/band_recommend.py
from sqlalchemy import Column, Integer, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from app.core.db import Base


class BandRecommend(Base):
    """band_recommend 테이블 매핑 - 추천된 밴드 저장"""
    __tablename__ = "band_recommend"

    id = Column("band_recommend_id", Integer, primary_key=True, index=True)
    priority = Column(Integer, nullable=True)
    score = Column(Float, nullable=True)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False, index=True)
    band_id = Column(Integer, ForeignKey("band.band_id"), nullable=False, index=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    member = relationship("Member", back_populates="band_recommends")
    band = relationship("Band")
