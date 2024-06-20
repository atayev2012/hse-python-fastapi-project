from typing import Annotated, Union
from sqlalchemy.orm import Session
from sqlalchemy import func
# from db_app.models import UserAccessLevel, User, Series, MySeries
# from user_app.schemas import UserFound, MySeriesForUserFound
from fastapi import HTTPException, status
from bcrypt import hashpw, gensalt, checkpw
from uuid import UUID


def str_to_uuid(uuid_code: str):
    return UUID(hex=uuid_code, version=4)


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



