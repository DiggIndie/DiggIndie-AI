# app/models/member.py
from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP
from sqlalchemy.orm import relationship

from app.core.db import Base


class Member(Base):
    """member 테이블 매핑"""
    __tablename__ = "member"

    id = Column("member_id", Integer, primary_key=True, index=True)
    external_id = Column(String(36), nullable=False, unique=True, index=True)
    role = Column(String(20), nullable=True)
    recent_login_platform = Column(String(20), nullable=True)
    user_id = Column("user_id", String(50), nullable=False)
    password = Column(String(100), nullable=True)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    profile_img = Column(String(150), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    member_bands = relationship("MemberBand", back_populates="member")
    member_keywords = relationship("MemberKeyword", back_populates="member")
    band_recommends = relationship("BandRecommend", back_populates="member")
