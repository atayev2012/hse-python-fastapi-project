from pydantic import BaseModel, Field
from typing import Annotated
from uuid import UUID
from datetime import datetime


class AddNewSeries(BaseModel):
    title: str = Field(max_length=64, examples=["The Dark Knight Rises"])
    description: str = Field(max_length=255, examples=["Eight years after the Joker's reign of chaos, Batman is "
                                                       "coerced out of exile with the assistance of the mysterious "
                                                       "Selina Kyle in order to defend Gotham City from the vicious "
                                                       "guerrilla terrorist Bane."])
    year: int = Field(ge=1888, le=3000, examples=[2012])


class GetEpisodes(BaseModel):
    id: UUID
    title: str
    description: str
    season_number: int
    episode_number: int


class GetSeriesInfo(BaseModel):
    id: UUID
    title: str
    description: str
    year: int
    episodes: list[GetEpisodes]


class UpdateSeries(BaseModel):
    id: UUID
    title: str | None = Field(None, examples=["Friends"])
    description: str | None = Field(None, examples=["Some friends fooling around"])
    year: int | None = Field(None, ge=1888, le=3000, examples=[2012])
