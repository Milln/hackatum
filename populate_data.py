from typing import Literal
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from datetime import date, datetime, timedelta
import random

from repository import Genre, User, Movie, ViewHistory


# Define some random data generators
adjectives = [
    "Dark",
    "Bright",
    "Hidden",
    "Eternal",
    "Mysterious",
    "Lost",
    "Forbidden",
    "Majestic",
    "Shattered",
    "Infinite",
    "Silent",
    "Dangerous",
    "Golden",
    "Savage",
    "Ancient",
    "Forgotten",
    "Secret",
    "Enchanted",
]
nouns = [
    "Forest",
    "Kingdom",
    "Legacy",
    "Journey",
    "Revenge",
    "Storm",
    "Shadow",
    "Truth",
    "Fire",
    "Dream",
    "Night",
    "Path",
    "Warrior",
    "Destiny",
    "Fortune",
    "Lies",
    "Winds",
    "Memory",
    "Haven",
    "Saga",
]
subscription_types = ["BASIC", "PREMIUM", "DEVELOPER"]
genres_list = [
    "Action",
    "Adventure",
    "Comedy",
    "Drama",
    "Horror",
    "Sci-Fi",
    "Romance",
    "Thriller",
    "Fantasy",
    "Mystery",
    "Crime",
    "Documentary",
    "Biography",
    "Music",
    "Family",
    "Animation",
    "Western",
    "History",
    "War",
    "Sport",
]
first_names = [
    "John",
    "Jane",
    "Alice",
    "Bob",
    "Charlie",
    "Diana",
    "Eve",
    "Frank",
    "Grace",
    "Hank",
]
surnames = [
    "Smith",
    "Johnson",
    "Brown",
    "Williams",
    "Jones",
    "Miller",
    "Davis",
    "Garcia",
    "Wilson",
    "Taylor",
]

NUM_USERS = 10
NUM_MOVIES = 100


def populate_database_random(engine: Engine):
    random.seed(1337)

    Session = sessionmaker(bind=engine)
    session = Session()

    def generate_random_movie_names(num_movies: int = NUM_MOVIES):
        unique_movie_names = set()
        while (
            len(unique_movie_names) < num_movies
        ):  # Ensure exactly 10 unique combinations
            first_part = random.choice(adjectives)
            last_part = random.choice(nouns)
            unique_movie_names.add(f"{first_part} {last_part}")
        return unique_movie_names

    def generate_random_names(num_names: int = NUM_USERS):
        unique_name_pairs = set()
        while (
            len(unique_name_pairs) < num_names
        ):  # Ensure exactly 10 unique combinations
            first_name = random.choice(first_names)
            surname = random.choice(surnames)
            unique_name_pairs.add((first_name, surname))
        return unique_name_pairs

    def get_status(date: date) -> Literal["AVAILABLE", "EXPIRED", "NOT_YET_RELEASED"]:
        if date > date.today():
            return "NOT_YET_RELEASED"
        if date + timedelta(days=365) > date.today():
            return "AVAILABLE"
        return "EXPIRED"

    # Insert genre data
    for genre_id, genre_name in enumerate(genres_list):
        session.add(Genre(id=genre_id, name=genre_name))

    session.commit()

    # Insert movie data
    all_genres = session.query(Genre).all()  # Fetch all genres
    movie_names = generate_random_movie_names(NUM_MOVIES)
    for i, name in enumerate(movie_names):  # Insert 100 movies
        release_date = (
            datetime(random.randint(2016, 2025), 1, 1)
            + timedelta(days=random.randint(0, 365))
        ).date()
        subscription_type = random.choice(subscription_types)
        license_cost = random.randint(1000, 500000)
        num_views = random.randint(1, 10000)
        popularity_rating = random.randint(1, 10)
        status = get_status(release_date)
        num_genres = random.randint(1, 3)

        movie = Movie(
            id=i,
            name=name,
            release_date=release_date,
            subscription_type=subscription_type,
            license_cost=license_cost,
            num_views=num_views,
            popularity_rating=popularity_rating,
            status=status,
            genres=random.sample(all_genres, num_genres),  # 1-3 genres
        )

        session.add(movie)

    session.commit()

    # Insert user data
    user_names = generate_random_names(NUM_USERS)
    for i, (surname, last_name) in enumerate(user_names):  # Insert 10 users
        gender = random.choice(["Male", "Female"])
        birthdate = (
            datetime(1990, 1, 1) + timedelta(days=random.randint(0, 365 * 30))
        ).date()  # Random birthdate
        phone_number = f"123-456-789{i}"
        email = f"{surname}.{last_name}@mail.de"
        country = "Germany"
        home_ip = f"192.168.1.{random.randint(1, 254)}"
        subscription_type = random.choice(subscription_types)

        user = User(
            id=i,
            surname=surname,
            last_name=last_name,
            gender=gender,
            birthdate=birthdate,
            phone_number=phone_number,
            email=email,
            country=country,
            home_ip_address=home_ip,
            subscription_type=subscription_type,
            hashed_password="supersecrethashedpassword",
        )

        session.add(user)

    session.commit()

    for user_id in range(NUM_USERS):
        # Insert random search and viewing history for the user
        for _ in range(random.randint(1, 5)):  # Random number of views
            timestamp = datetime.today() - timedelta(days=random.randint(0, 365))

            view_history_entry = ViewHistory(
                user_id=user_id,
                movie_id=random.choice(range(NUM_MOVIES)),
                view_timestamp=datetime.now(),  # Use current timestamp
                device=random.choice(["Smartphone", "Tablet", "PC", "Fridge"]),
                location="Germany",
                timestamp=timestamp,
            )

            # Add the record to the session and commit
            session.add(view_history_entry)

    session.commit()

    # Close the session
    session.close()

    print("Database populated successfully!")
