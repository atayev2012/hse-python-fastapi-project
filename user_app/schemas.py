from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(examples=["barracuda"], max_length=64, min_length=6,
                          description="username should be string with length between 6 and 64 characters")
    access_level: str = Field(examples=["moderator"], max_length=64,
                              description="Choose between 'user' and 'moderator'")


class AccessLevelCreate(BaseModel):
    level_description: str = Field(max_length=255, description="description of user level like admin or moderator")

