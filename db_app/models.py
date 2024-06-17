from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Column, ForeignKey, Float
from sqlalchemy.orm import DeclarativeBase, relationship
from .database import Base


class UserAccessLevel(Base):
    __tablename__ = "user_access_levels"

    id = Column(Integer, primary_key=True)
    level_description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())

    users = relationship("User", back_populates="user_level")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    access_level_id = Column(Integer, ForeignKey("user_access_levels.id"))

    my_series = relationship("MySeries", back_populates="owner")
    user_level = relationship("UserAccessLevel", back_populates="users")


class Series(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    year = Column(Integer)
    episode_qty = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())


class MySeries(Base):
    __tablename__ = "my_series"

    user_id = Column(Integer, ForeignKey("users.id"))
    series_id = Column(Integer, ForeignKey("series.id"))
    watched_episode_no = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow())

    owner = relationship("User", back_populates="my_series")


class SeriesRating(Base):
    __tablename__ = "series_rating"

    id = Column(Integer, primary_key=True)
    series_id = Column(Integer, ForeignKey("series.id"))
    rating = Column(Float(precision=5, decimal_return_scale=2), default=0)
    rated_qty = Column(Integer, default=0)

    ratings = relationship("SeriesRatingUser", back_populates="series_rating")


class SeriesRatingUser(Base):
    __tablename__ = "series_rating_user"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    series_id = Column(Integer, ForeignKey("series.id"))
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())

    series_rating = relationship("SeriesRating", back_populates="ratings")
