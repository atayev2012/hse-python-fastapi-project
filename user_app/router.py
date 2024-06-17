from fastapi import APIRouter, status
from sqlalchemy import Session
from db_app import models
from user_app.schemas import UserCreate, AccessLevelCreate


router = APIRouter(
    prefix="/user",
    tags=["User Info"]
)


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
def create_user():
    pass


@router.put("/update-user", status_code=status.HTTP_200_OK)
def update_user():
    pass


@router.delete("/delete-user", status_code=status.HTTP_200_OK)
def delete_user():
    pass


@router.get("/info-user", status_code=status.HTTP_200_OK)
def get_user(db: Session):
    pass
