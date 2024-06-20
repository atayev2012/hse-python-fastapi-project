from typing import Annotated, Union
from fastapi import APIRouter, status, Depends, Header, HTTPException, Response
from db_app.database import get_db
from db_app.models import User
from sqlalchemy.orm import Session
from user_app.utils import hash_password, password_hash_compare, str_to_uuid
from user_app.schemas import UserInfoResponse
# from db_app import models



router = APIRouter(
    prefix="/user",
    tags=["User Info"]
)


@router.post("/create-user", status_code=status.HTTP_201_CREATED)
def create_user(
        username: Annotated[str | None, Header(alias="username")],
        password: Annotated[str | None, Header(alias="password")],
        email: Annotated[str | None, Header(alias="email")],
        response: Response,
        session: Session = Depends(get_db)
):
    passkey_hash = hash_password(password)
    new_user = User(username=username, email=email, hashed_password=passkey_hash)
    session.add(new_user)
    session.commit()

    response.headers["User-Id"] = new_user.id.__str__()
    return {
        "status": "success",
        "message": "User was successfully created"
    }



@router.put("/update-user", status_code=status.HTTP_200_OK)
def update_user(email: str | None,
                user_id: Annotated[str | None, Header(alias="User-Id")],
                session: Session = Depends(get_db)
):

    user = session.get(User, str_to_uuid(user_id))
    user.email = email
    session.commit()

    return {
        "status": "success",
        "message": f"User email address was successfully changed to {email}"
    }


@router.delete("/delete-user", status_code=status.HTTP_200_OK)
def delete_user(
        user_id: Annotated[str | None, Header(alias="User-Id")],
        session: Session = Depends(get_db)
):
    user = session.get(User, str_to_uuid(user_id))
    session.delete(user)
    session.commit()
    return {
        "status": "success",
        "message": f"User was successfully deleted"
    }


@router.get("/info-user", status_code=status.HTTP_200_OK, response_model=UserInfoResponse)
def get_user(
        user_id: Annotated[str | None, Header(alias="User-Id")],
        session: Session = Depends(get_db)
):
    user = session.get(User, str_to_uuid(user_id))
    return user


@router.get("/info-users-all", status_code=status.HTTP_200_OK, response_model=list[UserInfoResponse])
def get_all_users(
        session: Session = Depends(get_db)
):
    users = session.query(User).all()
    return users
