from typing import Annotated
from sqlalchemy import UniqueConstraint, ForeignKey
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


class Series(Base):
    __tablename__ = "series"

    id: Mapped[uuid_pk]
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    year: Mapped[int]
    created_by: Mapped[UUID]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    episodes: Mapped[list["Episode"]] = relationship()

    __table_args__ = (UniqueConstraint('title', 'year', name='uix_title_year'),)


class Episode(Base):
    __tablename__ = "episodes"

    id: Mapped[uuid_pk]
    series_id: Mapped[UUID] = mapped_column(ForeignKey("series.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    episode_number: Mapped[int] = mapped_column(nullable=False)
    season_number: Mapped[int] = mapped_column(nullable=False)
    created_by: Mapped[UUID]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    series: Mapped["Series"] = relationship()

    __table_args__ = (UniqueConstraint('series_id', 'episode_number', "season_number", name='uix_title_year'),)

    #     description = Column(String)
    #     episode_number = Column(Integer)
    #     season_number = Column(Integer)
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