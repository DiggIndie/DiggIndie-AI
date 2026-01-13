# app/models/member_band.py
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from app.core.db import Base


class MemberBand(Base):
    """member_band 테이블 매핑 - 사용자가 선택한 밴드"""
    __tablename__ = "member_band"

    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False, index=True)
    band_id = Column(Integer, ForeignKey("band.band_id"), nullable=True, index=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    member = relationship("Member", back_populates="member_bands")
    band = relationship("Band")
