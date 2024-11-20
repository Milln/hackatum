from sqlalchemy import (
    Column,
    Engine,
    Integer,
    String,
    Date,
    ForeignKey,
    Enum,
    DateTime,
    Table,
)
from sqlalchemy.orm import declarative_base, relationship
import enum
from datetime import datetime


Base = declarative_base()


# Enums for subscription type and movie status
class SubscriptionType(enum.Enum):
    BASIC = "Basic"
    PREMIUM = "Premium"
    DEVELOPER = "Developer"


class MovieStatus(enum.Enum):
    AVAILABLE = "Available"
    EXPIRED = "Expired"
    NOT_YET_RELEASED = "Not Yet Released"


# Association table for the many-to-many relationship between Movies and Genres
movie_genre_table = Table(
    "movie_genre",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movie.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genre.id"), primary_key=True),
)


# Movie table
class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    release_date = Column(Date, nullable=False)
    subscription_type = Column(Enum(SubscriptionType), nullable=False)
    license_cost = Column(Integer, nullable=False)
    num_views = Column(Integer, default=0)
    popularity_rating = Column(Integer, default=0)
    status = Column(Enum(MovieStatus), nullable=False, default=MovieStatus.AVAILABLE)
    genres = relationship("Genre", secondary=movie_genre_table, back_populates="movies")


# User table
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    surname = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    country = Column(String, nullable=False)
    home_ip_address = Column(String, nullable=True)
    subscription_type = Column(Enum(SubscriptionType), nullable=False)
    viewing_history = relationship("ViewingHistory", back_populates="user")
    search_history = relationship("SearchHistory", back_populates="user")


# Subscription table
class Subscription(Base):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True)
    name = Column(Enum(SubscriptionType), unique=True, nullable=False)


# Genre table
class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    movies = relationship("Movie", secondary=movie_genre_table, back_populates="genres")


# Viewing History table
class ViewingHistory(Base):
    __tablename__ = "viewing_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movie.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    user = relationship("User", back_populates="viewing_history")
    movie = relationship("Movie")


# Search History table
class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    search_query = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    user = relationship("User", back_populates="search_history")


def create_database(engine: Engine):
    Base.metadata.create_all(engine)
