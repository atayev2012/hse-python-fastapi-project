from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class UserInfoResponse(BaseModel):
    id: UUID
    username: str
    email: str
    created_at: datetime
