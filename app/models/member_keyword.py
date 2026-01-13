# app/models/member_keyword.py
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from app.core.db import Base


class MemberKeyword(Base):
    """member_keyword 테이블 매핑 - 사용자가 선택한 키워드"""
    __tablename__ = "member_keyword"

    id = Column("member_keyword_id", Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("member.member_id"), nullable=False, index=True)
    keyword_id = Column(Integer, ForeignKey("keyword.keyword_id"), nullable=False, index=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)

    # Relationships
    member = relationship("Member", back_populates="member_keywords")
    keyword = relationship("Keyword")
