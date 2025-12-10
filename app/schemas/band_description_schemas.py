from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class BandDescriptionResponse(BaseModel):
    band_id: int
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    embedding: Optional[List[float]] = None
