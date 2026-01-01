# app/models/keyword.py
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

from app.core.db import Base


class Keyword(Base):
    """keyword 테이블 매핑"""
    __tablename__ = "keyword"

    id = Column("keyword_id", Integer, primary_key=True, index=True)
    keyword = Column(String(20), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relationship with BandKeyword
    band_keywords = relationship("BandKeyword", back_populates="keyword")


class BandKeyword(Base):
    """
    band_keyword 테이블 매핑
    Band와 Keyword 간의 다대다 관계를 위한 중간 테이블
    """
    __tablename__ = "band_keyword"

    id = Column("band_keyword_id", Integer, primary_key=True, index=True)
    band_id = Column(Integer, ForeignKey("band.band_id"), nullable=False, index=True)
    keyword_id = Column(Integer, ForeignKey("keyword.keyword_id"), nullable=False, index=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    band = relationship("Band", back_populates="band_keywords")
    keyword = relationship("Keyword", back_populates="band_keywords")
