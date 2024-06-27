from fastapi import APIRouter, Depends, Header, status
from db_app.models import UserSeries, UserEpisode, User, Series, Episode
from db_app.database import get_db
from sqlalchemy.orm import Session, selectinload, joinedload
from typing import Annotated
from user_app.utils import str_to_uuid, verify_item_exists
from series_app.utils import raise_http_exception
from track_app.schemas import WatchedUserEpisode


router = APIRouter(
    prefix="/track",
    tags=["Tracking"]
)


@router.post("/add-episode")
def add_episode(
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
    series_uuid = episode.series_id

    # check if user already watching this series
    user_series = session.query(UserSeries).filter(UserSeries.series_id == series_uuid).first()
    print(user_series)
    if not user_series:
        user_series = UserSeries(
            user_id=user_uuid,
            series_id=series_uuid
        )

        user_episode = UserEpisode(
            user_id=user_uuid,
            episode_id=episode_uuid,
            series_id=series_uuid
        )

        session.add(user_series)
        session.add(user_episode)
        session.commit()

    else:

        try:
            user_episode = UserEpisode(
                user_id=user_uuid,
                episode_id=episode_uuid,
                series_id=series_uuid
            )

            session.add(user_episode)
            session.commit()
        except Exception as e:
            raise_http_exception(
                status.HTTP_400_BAD_REQUEST,
                e
            )


    return {
        "status": "success"
    }

@router.delete("/delete-episode")
def delete_episode(
        user_id: Annotated[str, Header(alias="User-Id")],
        user_episode_id: str,
        session: Session = Depends(get_db)
):
    # convert str ids to UUID
    user_uuid = str_to_uuid(user_id)
    user_episode_uuid = str_to_uuid(user_episode_id)

    # verification of user
    verify_item_exists(user_uuid, User, "User", session)
    user_episode = verify_item_exists(user_episode_uuid, UserEpisode, "UserEpisode", session)

    session.delete(user_episode)
    session.commit()

    return {
        "status":  "success"
    }

@router.get("/get-user-series", response_model=list[WatchedUserEpisode])
def get_user_series(
        user_id: Annotated[str, Header(alias="User-Id")],
        session: Session = Depends(get_db)
):
    # convert str ids to UUID
    user_uuid = str_to_uuid(user_id)

    # verification of user
    user = verify_item_exists(user_uuid, User, "User", session)

    # users = session.query(User).options(
    #     selectinload(User.series).selectinload(UserSeries.series).selectinload(UserSeries.user_episodes)
    #     # joinedload(UserSeries.series).joinedload(UserEpisode.episode)
    # ).all()
    return user.watched_series

