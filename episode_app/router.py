from typing import Annotated
from fastapi import APIRouter, Depends, Header
from db_app.database import get_db
from db_app.models import User, Series, Episode
from sqlalchemy.orm import Session
from user_app.utils import str_to_uuid, verify_item_exists
from episode_app.schemas import AddEpisode, UpdateEpisode

router = APIRouter(
    prefix="/episodes",
    tags=["Series episodes"]
)


@router.post("/add-episode")
def add_episode(
        episode_info: AddEpisode,
        user_id: Annotated[str, Header(alias="User-Id")],
        session: Session = Depends(get_db)
):
    # convert str ids to UUID
    user_uuid = str_to_uuid(user_id)

    # verification of user
    verify_item_exists(user_uuid, User, "User", session)
    verify_item_exists(episode_info.series_id, Series, "Series", session)

    episode = Episode(
        series_id=episode_info.series_id,
        title=episode_info.title,
        description=episode_info.description,
        episode_number=episode_info.episode_number,
        sesason_number=episode_info.season_number
    )

    session.add(episode)
    session.commit()

    return episode


@router.put("/update-episode")
def update_episode(
        episode_info: UpdateEpisode,
        user_id: Annotated[str, Header(alias="User-Id")],
        session: Session = Depends(get_db)
):
    # convert str ids to UUID
    user_uuid = str_to_uuid(user_id)

    # verification of user
    verify_item_exists(user_uuid, User, "User", session)
    episode = verify_item_exists(episode_info.id, Episode, "Episode", session)

    if episode_info.title:
        episode.title = episode_info.title

    if episode_info.description:
        episode.description = episode_info.description

    if episode_info.episode_number:
        episode.episode_number = episode_info.episode_number

    if episode_info.season_number:
        episode.season_number = episode_info.season_number

    session.commit()

    return episode

@router.delete("/delete-episode")
def delete_episode(
        episode_id: str,
        user_id: Annotated[str, Header(alias="User-Id")],
        session: Session = Depends(get_db)
):
    # convert str ids to UUID
    user_uuid = str_to_uuid(user_id)
    episode_uuid = str_to_uuid(episode_id)
    # verification of user
    verify_item_exists(user_uuid, User, "User", session)
    episode = verify_item_exists(episode_uuid, Episode, "Episode", session)

    session.delete(episode)
    session.commit()

    return {
        "status": "success",
        "message": "Episode was successfully deleted"
    }

@router.get("/get-episode")
def get_episode(
        episode_id: str,
        user_id: Annotated[str, Header(alias="User-Id")],
        session: Session = Depends(get_db)
):
    # convert str ids to UUID
    user_uuid = str_to_uuid(user_id)
    episode_uuid = str_to_uuid(episode_id)
    # verification of user
    verify_item_exists(user_uuid, User, "User", session)
    episode = verify_item_exists(episode_uuid, Episode, "Episode", session)

    return episode

@router.get("/get-episodes-all")
def get_all_episodes(
        user_id: Annotated[str, Header(alias="User-Id")],
        session: Session = Depends(get_db)
):
    # convert str ids to UUID
    user_uuid = str_to_uuid(user_id)
    # verification of user
    verify_item_exists(user_uuid, User, "User", session)
    episodes = session.query(Episode).all()

    return episodes
