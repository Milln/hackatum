import os
from sqlalchemy import (
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
    text,
)
from sqlalchemy.orm import relationship, declarative_base


# Define the database engine and base class for ORM
Base = declarative_base()


# User Table
class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    subscription_type = Column(String, nullable=False)

    # Relationships
    watch_history = relationship("WatchHistory", back_populates="user")


# Watch History Table
class WatchHistory(Base):
    __tablename__ = "watch_history"

    history_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movie.movie_id"), nullable=False)
    watched_on = Column(Date, nullable=False)

    # Relationships
    user = relationship("User", back_populates="watch_history")
    movie = relationship("Movie", back_populates="watch_history")


# Movie Table
class Movie(Base):
    __tablename__ = "movie"

    movie_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    release_date = Column(Date, nullable=True)
    licence_cost = Column(Float, nullable=True)
    content_expiry = Column(Date, nullable=True)

    # Relationships
    watch_history = relationship("WatchHistory", back_populates="movie")


# Genre Table
class Genre(Base):
    __tablename__ = "genre"

    genre_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


# License Providers Table
class LicenseProvider(Base):
    __tablename__ = "license_providers"

    provider_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    license_fee = Column(Float, nullable=False)


# Create all tables in the database
class StreamingDatabase:
    DATABASE_PATH = "streaming_service.db"
    POPULATION_SCRIPT_PATH = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "populate_data.sql"
    )

    def __init__(self, echo: bool = False) -> None:
        self.echo = echo
        self.create_database()

    def create_database(self):
        self.engine = create_engine(f"sqlite:///{self.DATABASE_PATH}", echo=self.echo)
        Base.metadata.create_all(self.engine)

    def populate_database(self):
        print("Populating database...")
        try:
            os.remove(self.DATABASE_PATH)
            print("Recreating database!")
            self.create_database()
        except OSError:
            pass

        with open(self.POPULATION_SCRIPT_PATH, "r") as file:
            sql_script = file.read()

        # Connect to the database and execute the script
        with self.engine.connect() as connection:
            for statement in sql_script.split(";"):
                if statement.strip():
                    connection.execute(text(statement.strip()))
            connection.commit()
        print("Database populated!")


if __name__ == "__main__":
    db = StreamingDatabase()
    db.populate_database()

    with db.engine.connect() as con:
        rows = con.execute(text("SELECT title from movie"))
        for row in rows:
            print(row)
