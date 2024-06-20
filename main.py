from fastapi import FastAPI
from user_app.router import router as user_app_router
from db_app.database import SessionLocal, engine, Base
# from db_app.models import User, UserAccessLevel, Series, MySeries, SeriesRating, SeriesRatingUser


# from series_app.router import router as series_app_router
# create database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_app_router)
# app.include_router(series_app_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

