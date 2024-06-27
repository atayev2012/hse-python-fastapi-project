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

    watched_series: Mapped[list["UserSeries"]] = relationship(back_populates="user")


class Series(Base):
    __tablename__ = "series"

    id: Mapped[uuid_pk]
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]
    year: Mapped[int]
    rating: Mapped[float] = mapped_column(default=0)
    rating_qty: Mapped[int] = mapped_column(default=0)
    created_by: Mapped[UUID]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    episodes: Mapped[list["Episode"]] = relationship(back_populates="series", cascade='all, delete-orphan')
    rating: Mapped[list["RatingHistory"]] = relationship(back_populates="series", cascade='all, delete-orphan')

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

    series: Mapped["Series"] = relationship(back_populates="episodes")

    __table_args__ = (UniqueConstraint('series_id', 'episode_number', "season_number", name='uix_title_year'),)


class UserSeries(Base):
    __tablename__ = "user_series"

    id: Mapped[uuid_pk]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    series_id: Mapped[UUID] = mapped_column(ForeignKey("series.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    user: Mapped["User"] = relationship()
    series: Mapped["Series"] = relationship()
    user_episodes: Mapped[list["Episode"]] = relationship(
        secondary="user_episode",
        primaryjoin="UserEpisode.user_id==UserSeries.user_id",
        secondaryjoin="and_(UserEpisode.series_id==Episode.series_id, UserEpisode.episode_id==Episode.id)",
    )


class UserEpisode(Base):
    __tablename__ = "user_episode"

    id: Mapped[uuid_pk]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    series_id: Mapped[UUID] = mapped_column(ForeignKey("series.id", ondelete="CASCADE"))
    episode_id: Mapped[UUID] = mapped_column(ForeignKey("episodes.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    __table_args__ = (UniqueConstraint("user_id", "series_id", "episode_id", name="user_series_episodes"),)

class RatingHistory(Base):
    __tablename__ = "rating_history"

    id: Mapped[uuid_pk]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    series_id: Mapped[UUID] = mapped_column(ForeignKey("series.id", ondelete="CASCADE"))
    rating_value: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    series: Mapped[Series] = relationship()

    __table_args__ = (UniqueConstraint("user_id", "series_id", name="user_series"),)