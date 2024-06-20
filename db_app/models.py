from typing import Annotated
from sqlalchemy import Integer, String, DateTime, Column, ForeignKey, Float, func, text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db_app.database import Base
from datetime import datetime
from uuid import UUID, uuid4

uuid_pk = Annotated[UUID, mapped_column(primary_key=True, default=uuid4, index=True)]
created_at = Annotated[datetime, mapped_column(default=datetime.utcnow)]
updated_at = Annotated[datetime, mapped_column(
    default=datetime.utcnow,
    onupdate=datetime.utcnow
)]


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid_pk]
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[created_at]

    # series_watched: Mapped[list["SeriesWatchTrack"]] = relationship()

#
# class SeriesWatchTrack(Base):
#     __tablename__ = "series_watch_track"
#
#     id: Mapped[uuid_pk]
#     user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id",  ondelete="CASCADE"))
#     series_id: Mapped[UUID] = mapped_column(ForeignKey("series.id", ondelete="CASCADE"))
#     episode_id: Mapped[UUID] = mapped_column(ForeignKey("episodes.id", ondelete="CASCADE"))
#     created_at: Mapped[created_at]
#
#     user: Mapped["User"] = relationship()
#
#
# class Series(Base):
#     __tablename__ = "series"
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, unique=True, index=True, nullable=False)
#     description = Column(String)
#     year = Column(Integer)
#     added_at = Column(DateTime, server_default=func.now())
#
#     episodes = relationship("Episode", back_populates="series")
#     ratings = relationship("UserSeriesRating", back_populates="series")
#
#
#
# class Episode(Base):
#     __tablename__ = "episodes"
#
#     id = Column(Integer, primary_key=True, index=True)
#     series_id = Column(Integer, ForeignKey("series.id"), nullable=False)
#     title = Column(String, nullable=False)
#     description = Column(String)
#     episode_number = Column(Integer)
#     season_number = Column(Integer)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#
#     series = relationship("Series", back_populates="episodes")
#
#
# class UserSeriesRating(Base):
#     __tablename__ = "user_series_ratings"
#
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     series_id = Column(Integer, ForeignKey("series.id"), nullable=False)
#     rating = Column(Float, nullable=True)
#     watched_episodes = Column(Integer, default=0)
#     watched_at = Column(DateTime(timezone=True), server_default=func.now())
#
#     user = relationship("User", back_populates="ratings")
#     series = relationship("Series", back_populates="ratings")