from fastapi import APIRouter, Depends, Header, status
from db_app.models import UserSeries, UserEpisode, User, Series, Episode, RatingHistory
from db_app.database import get_db
from sqlalchemy.orm import Session, selectinload, joinedload
from typing import Annotated
from user_app.utils import str_to_uuid, verify_item_exists
from rate_app.schemas import RateSeries
from sqlalchemy.exc import SQLAlchemyError
from series_app.utils import raise_http_exception
from track_app.schemas import WatchedUserEpisode

router = APIRouter(
    prefix="/rating",
    tags=["Rating Series"]
)

@router.post("/rate")
def add_episode(
        user_id: Annotated[str, Header(alias="User-Id")],
        rating_data: RateSeries,
        session: Session = Depends(get_db)
):
    # convert str ids to UUID
    user_uuid = str_to_uuid(user_id)
    series_uuid = rating_data.series_id

    # verification of user
    verify_item_exists(user_uuid, User, "User", session)
    series = verify_item_exists(series_uuid, Series, "Series", session)

    # check if rating already exist
    rating = session.query(RatingHistory).filter(RatingHistory.user_id == user_uuid).filter(RatingHistory.series_id == series_uuid).first()

    if rating:
        try:
            # change value in series table
            series.rating = (series.rating * series.rating_qty - rating.rating_value + rating_data.rating) / series.rating_qty

            # need to update if exist
            rating.rating_value = rating_data.rating

            session.commit()

        except SQLAlchemyError as e:
            raise_http_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, e)

        return{
            "status": "success",
            "message": "Series rating was successfully updated",
            "data": {
                "series_id": series.id,
                "title": series.title,
                "rating": f"{series.rating: .2f}"
            }
        }

    try:
        rating = RatingHistory(user_id=user_uuid, series_id=series_uuid, rating_value=rating_data.rating)

        if series.rating == 0:
            series.rating = rating_data.rating
        else:
            series.rating = (series.rating * series.rating_qty + rating_data.rating) / (series.rating_qty + 1)
        series.rating_qty += 1

        session.add(rating)
        session.commit()

    except SQLAlchemyError as e:
        raise_http_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, e)

    return {
        "status": "success",
        "message": "Series was successfully rated",
        "data": {
            "series_id": series.id,
            "title": series.title,
            "rating": f"{series.rating: .2f}"
        }
    }

