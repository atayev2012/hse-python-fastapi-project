from typing import Annotated, Union
from sqlalchemy.orm import Session
from sqlalchemy import func
from db_app.models import User
# from user_app.schemas import UserFound, MySeriesForUserFound
from fastapi import HTTPException, status
from bcrypt import hashpw, gensalt, checkpw
from uuid import UUID
from db_app.database import Base


# convert user id str from database to UUID variable
def str_to_uuid(uuid_code: str):
    try:
        user_uuid = UUID(hex=uuid_code, version=4)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "fail",
                "message": "UUID-ERROR: " + e.args[0],
                "data": None
            }
        )
    return user_uuid


# verify that user exists
def verify_item_exists(item_uuid: UUID, item_class: Base, msg_name: str, session: Session) -> Base | None:
    user = session.get(item_class, item_uuid)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=dict(status="fail",
                        message=f"{msg_name} "
                                f"Error: no {msg_name.lower()} "
                                f"with provided id was found",
                        data=None)
        )

    return user


def hash_password(password: str) -> str:
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")


def password_hash_compare(password: str, password_hash: str):
    hash_val = password_hash.encode("utf-8")
    pass_val = password.encode("utf-8")
    return checkpw(pass_val, hash_val)


if __name__ == "__main__":
    pass_key = input("Enter password: ")
    hash_val = hash_password(pass_key)

    print(f"hash: {hash_val}")

    new_pass_key = input("New pass: ")

    print(password_hash_compare(new_pass_key, hash_val))



