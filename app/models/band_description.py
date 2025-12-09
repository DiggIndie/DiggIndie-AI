# app/models/band_description.py
from sqlalchemy import Column, Integer, Text, TIMESTAMP
from pgvector.sqlalchemy import VECTOR

from app.core.db import Base

class BandDescription(Base):
    __tablename__ = "band_description"

    band_id = Column(Integer, primary_key=True, index=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    description = Column(Text, nullable=True)
    embedding = Column(VECTOR(1536), nullable=True)
