from pydantic import BaseModel, Field
from uuid import UUID


class AddEpisode(BaseModel):
    series_id: UUID
    title: str | None = Field(None, examples=["Ходячие мертвецы"], max_length=64)
    description: str | None = Field(None, examples=["Однажды на Землю обрушивается неизвестный вирус, который "
                                                    "обращает большую часть населения в кровожадных зомби. С "
                                                    "этого момента цивилизация рушиться и на ее осколках выжившие "
                                                    "сражаются с теми, кто еще недавно был их родственниками и "
                                                    "друзьями."], max_length=255)
    episode_number: int = Field(ge=0, examples=[1])
    season_number: int = Field(ge=0, examples=[1])


class UpdateEpisode(BaseModel):
    id: UUID
    title: str | None = Field(None, examples=["Ходячие мертвецы"], max_length=64)
    description: str | None = Field(None, examples=["Однажды на Землю обрушивается неизвестный вирус, который "
                                                    "обращает большую часть населения в кровожадных зомби. С "
                                                    "этого момента цивилизация рушиться и на ее осколках выжившие "
                                                    "сражаются с теми, кто еще недавно был их родственниками и "
                                                    "друзьями."], max_length=255)
    episode_number: int | None = Field(None, ge=0, examples=[1])
    season_number: int | None = Field(None, ge=0, examples=[1])