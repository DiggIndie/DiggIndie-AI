from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class BandDescriptionResponse(BaseModel):
    band_id: int
    description: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    deletedAt: Optional[datetime] = None
    embedding: Optional[List[float]] = None
