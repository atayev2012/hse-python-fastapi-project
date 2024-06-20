from typing import Annotated, Union
from db_app.database import get_db
from db_app.models import Series, User
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from user_app.utils import str_to_uuid, verify_item_exists
from series_app.schemas import AddNewSeries, GetSeriesInfo, UpdateSeries
from series_app.utils import raise_http_exception
from fastapi import (APIRouter, status, Depends, Header, HTTPException, Response)

router = APIRouter(
    prefix="/series",
    tags=["Series"]
)


@router.get("/info-series", status_code=status.HTTP_200_OK, response_model=GetSeriesInfo)
def get_series(
        series_id: str,
        user_id: Annotated[str | None, Header(alias="User-Id")],
        session: Session = Depends(get_db)
):
    # convert str from db to uuid
    user_uuid = str_to_uuid(user_id)
    series_uuid = str_to_uuid(series_id)
    # check if user exists
    verify_item_exists(user_uuid, User, "User", session)
    verify_item_exists(series_uuid, Series, "Series", session)

    series = session.get(Series, series_uuid)

    return series


@router.get("/info-series-all", status_code=status.HTTP_200_OK, response_model=list[GetSeriesInfo])
def get_all_series(
        user_id: Annotated[str | None, Header(alias="User-Id")],
        session: Session = Depends(get_db)
):
    # convert str from db to uuid
    user_uuid = str_to_uuid(user_id)
    # check if user exists
    verify_item_exists(user_uuid, User, "User", session)

    series_all = session.query(Series).all()

    return series_all


@router.post("/add-series", status_code=status.HTTP_201_CREATED)
def add_series(
        series_info: AddNewSeries,
        user_id: Annotated[str | None, Header(alias="User-Id")],
        session: Session = Depends(get_db)
):
    # convert str from db to uuid
    user_uuid = str_to_uuid(user_id)
    # check if user exists
    verify_item_exists(user_uuid, User, "User", session)

    try:
        new_series = Series(
            title=series_info.title,
            description=series_info.description,
            year=series_info.year,
            created_by=user_uuid)
        session.add(new_series)
        session.commit()
    except SQLAlchemyError as e:
        raise_http_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, e)

    return {
        "status": "success",
        "message": f"Series was successfully added",
        "data": new_series
    }


@router.put("/update-series", status_code=status.HTTP_200_OK, response_model=GetSeriesInfo)
def update_series(
        series_data: UpdateSeries,
        user_id: Annotated[str | None, Header(alias="User-Id")],
        session: Session = Depends(get_db)
):
    # convert str from db to uuid
    user_uuid = str_to_uuid(user_id)
    # check if user exists
    verify_item_exists(user_uuid, User, "User", session)
    verify_item_exists(series_data.id, Series, "Series", session)

    series = session.get(Series, series_data.id)

    if series_data.title:
        series.title = series_data.title

    if series_data.description:
        series.description = series_data.description

    if series_data.year:
        series.year = series_data.year

    session.commit()

    return series


@router.delete("/delete-series", status_code=status.HTTP_200_OK)
def delete_series(
        series_id: str,
        user_id: Annotated[str | None, Header(alias="User-Id")],
        session: Session = Depends(get_db)
):
    # convert str from db to uuid
    user_uuid = str_to_uuid(user_id)
    series_uuid = str_to_uuid(series_id)
    # check if user exists
    verify_item_exists(user_uuid, User, "User", session)

    series = verify_item_exists(series_uuid, Series, "Series", session)

    session.delete(series)
    session.commit()

    return {
        "status": "success",
        "message": f"Series was successfully deleted"
    }
