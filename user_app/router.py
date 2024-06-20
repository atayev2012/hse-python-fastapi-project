from typing import Annotated, Union
from fastapi import APIRouter, status, Depends, Header, HTTPException
from db_app.database import get_db
from sqlalchemy.orm import Session
# from db_app import models



router = APIRouter(
    prefix="/user",
    tags=["User Info"]
)


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
def create_user(db: Session = Depends(get_db)):
    pass


@router.put("/update-user", status_code=status.HTTP_200_OK)
def update_user(db: Session = Depends(get_db)):
    pass


@router.delete("/delete-user", status_code=status.HTTP_200_OK)
def delete_user(db: Session = Depends(get_db)):
    pass


@router.get("/info-user", status_code=status.HTTP_200_OK)
    pass