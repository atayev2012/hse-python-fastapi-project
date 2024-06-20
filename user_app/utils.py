from typing import Annotated, Union
from sqlalchemy.orm import Session
from sqlalchemy import func
from db_app.models import UserAccessLevel, User, Series, MySeries
from user_app.schemas import UserFound, MySeriesForUserFound
from fastapi import HTTPException, status



