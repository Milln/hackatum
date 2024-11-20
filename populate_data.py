from typing import Literal
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from datetime import date, datetime, timedelta
import random

from repository import Genre, SearchHistory, User, ViewingHistory, Movie


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
subscription_types = ["Basic", "Premium", "Developer"]
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


def populate_database_random(engine: Engine):
    random.seed(1337)

    Session = sessionmaker(bind=engine)
    session = Session()

    def generate_random_movie_names(num_movies: int = 100):
        unique_movie_names = set()
        while (
            len(unique_movie_names) < num_movies
        ):  # Ensure exactly 10 unique combinations
            first_part = random.choice(adjectives)
            last_part = random.choice(nouns)
            unique_movie_names.add(f"{first_part} {last_part}")
        return unique_movie_names

    def generate_random_names(num_names: int = 10):
        unique_name_pairs = set()
        while (
            len(unique_name_pairs) < num_names
        ):  # Ensure exactly 10 unique combinations
            first_name = random.choice(first_names)
            surname = random.choice(surnames)
            unique_name_pairs.add((first_name, surname))
        return unique_name_pairs

    def get_status(date: date) -> Literal["Available", "Expired", "Not Yet Released"]:
        if date > date.today():
            return "Not Yet Released"
        if date + timedelta(days=365) > date.today():
            return "Available"
        return "Expired"

    # Insert genre data
    for genre_id, genre_name in enumerate(genres_list):
        session.add(Genre(id=genre_id, name=genre_name))

    session.commit()

    # Insert movie data
    all_genres = session.query(Genre).all()  # Fetch all genres
    movie_names = generate_random_movie_names(100)
    for i, name in enumerate(movie_names):  # Insert 100 movies
        release_date = (
            datetime(random.randint(2016, 2025), 1, 1)
            + timedelta(days=random.randint(0, 365))
        ).date()
        subscription_type = random.choice(subscription_types)
        license_cost = random.randint(1000, 50000)
        num_views = random.randint(1, 1000)
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
    user_names = generate_random_names(10)
    for i, (surname, last_name) in enumerate(user_names):  # Insert 10 users
        gender = random.choice(["Male", "Female"])
        birthdate = (
            datetime(1990, 1, 1) + timedelta(days=random.randint(0, 365 * 30))
        ).date()  # Random birthdate
        phone_number = f"123-456-789{i}"
        email = f"user{i}@example.com"
        country = "USA"
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

        # Insert random search and viewing history for the user
        for _ in range(random.randint(1, 5)):  # Random number of searches/views
            movie_id = random.randint(1, 100)  # Random movie ID
            timestamp = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))

            # Insert search history
            search_history = SearchHistory(
                user_id=i,
                timestamp=timestamp,
                search_query="Blub",
            )
            session.add(search_history)

            # Insert viewing history
            viewing_history = ViewingHistory(
                user_id=i, movie_id=movie_id, timestamp=timestamp
            )
            session.add(viewing_history)

    # Commit the session to persist the changes
    session.commit()

    # Close the session
    session.close()

    print("Database populated successfully!")
