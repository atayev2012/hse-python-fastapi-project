from pydantic import BaseModel
from db_app.models import UserSeries
from uuid import UUID



class WatchedEpisode(BaseModel):
    id: UUID
    title: str
    season_number: int
    episode_number: int
    description: str

class WatchedSeries(BaseModel):
    title: str
    year: int


class WatchedUserEpisode(BaseModel):
    series: WatchedSeries
    user_episodes: list[WatchedEpisode]
