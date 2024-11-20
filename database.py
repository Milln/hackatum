import os

from sqlalchemy import create_engine, text

from populate_data import populate_database_random
from repository import create_database


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
        create_database(self.engine)

    def populate_database(self):
        print("Populating database...")
        try:
            os.remove(self.DATABASE_PATH)
            print("Recreating database!")
            self.create_database()
        except OSError:
            pass

        populate_database_random(self.engine)

        print("Database populated!")


if __name__ == "__main__":
    db = StreamingDatabase()
    db.populate_database()

    # with db.engine.connect() as con:
    #     rows = con.execute(text("SELECT name from movie"))
    #     for row in rows:
    #         print(row)
