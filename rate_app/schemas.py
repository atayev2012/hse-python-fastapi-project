from pydantic import BaseModel, Field
from uuid import UUID


class RateSeries(BaseModel):
    series_id: UUID
    rating: int = Field(ge=1, le=5)
