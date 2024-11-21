from typing import Literal
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker

from datetime import date, datetime, timedelta
import random

from repository import Genre, SearchHistory, User, Movie, ViewHistory


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
    "Amazing",
    "Broken",
    "Clever",
    "Fantastic",
    "Glorious",
    "Invincible",
    "Jubilant",
    "Kind",
    "Legendary",
    "Noble",
    "Outstanding",
    "Powerful",
    "Quiet",
    "Radiant",
    "Timeless",
    "Unstoppable",
    "Vibrant",
    "Wondrous",
    "Xenial",
    "Young",
    "Zealous",
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
    "Adventure",
    "Battle",
    "Castle",
    "Empire",
    "Galaxy",
    "Hero",
    "Island",
    "Legend",
    "Mountain",
    "Night",
    "Odyssey",
    "Phantom",
    "Quest",
    "Treasure",
    "Universe",
    "Victory",
    "Whisper",
    "Xylophone",
    "Yearning",
    "Zenith",
]

subscription_types = ["BASIC", "PREMIUM", "DEVELOPER"]
genres = [
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
    "Emma",
    "Liam",
    "Olivia",
    "Noah",
    "Ava",
    "Sophia",
    "James",
]

last_names = [
    "Smith",
    "Johnson",
    "Brown",
    "Williams",
    "Jones",
    "Miller",
    "Davis",
    "Wilson",
    "Taylor",
    "Lopez",
    "Anderson",
]

devices = ["Smartphone", "Tablet", "PC", "Fridge"]
locations = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
]
genders = ["M", "F", "NA"]


DEFAULT_NUM_USERS = 10
DEFAULT_NUM_MOVIES = 200


def populate_database_random(
    engine: Engine,
    num_users: int = DEFAULT_NUM_USERS,
    num_movies: int = DEFAULT_NUM_MOVIES,
):
    random.seed(1337)

    Session = sessionmaker(bind=engine)
    session = Session()

    def generate_random_movie_names(num_movies: int):
        unique_movie_names = set()
        while (
            len(unique_movie_names) < num_movies
        ):  # Ensure exactly 10 unique combinations
            first_part = random.choice(adjectives)
            last_part = random.choice(nouns)
            unique_movie_names.add(f"{first_part} {last_part}")
        return unique_movie_names

    def generate_random_names(num_names: int):
        unique_name_pairs = set()
        while (
            len(unique_name_pairs) < num_names
        ):  # Ensure exactly 10 unique combinations
            first_name = random.choice(first_names)
            surname = random.choice(last_names)
            unique_name_pairs.add((first_name, surname))
        return unique_name_pairs

    def generate_random_ip():
        return ".".join(str(random.randint(0, 255)) for _ in range(4))

    def generate_random_phone_number():
        area_code = random.randint(200, 999)  # Area codes don't start with 0 or 1
        central_office_code = random.randint(
            200, 999
        )  # Central office codes don't start with 0 or 1
        line_number = random.randint(1000, 9999)
        return f"({area_code}) {central_office_code}-{line_number}"

    def get_status(date: date) -> Literal["AVAILABLE", "EXPIRED", "NOT_YET_RELEASED"]:
        if date > date.today():
            return "NOT_YET_RELEASED"
        if date + timedelta(days=365) > date.today():
            return "AVAILABLE"
        return "EXPIRED"

    # Insert genre data
    for genre_id, genre_name in enumerate(genres):
        session.add(Genre(id=genre_id, name=genre_name))

    session.commit()

    # Insert movie data
    all_genres = session.query(Genre).all()  # Fetch all genres
    movie_names = generate_random_movie_names(num_movies)
    for i, name in enumerate(movie_names):  # Insert 100 movies
        release_date = (
            datetime(random.randint(2018, 2026), 1, 1)
            + timedelta(days=random.randint(0, 365))
        ).date()  # 2018-2027
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
    user_names = generate_random_names(num_users)
    for i, (first_name, last_name) in enumerate(user_names):
        gender = random.choice(genders)
        birthdate = (
            datetime(1970, 1, 1)
            + timedelta(days=random.randint(0, 365 * 40))  # 1970-2010
        ).date()
        phone_number = generate_random_phone_number()
        email = f"{first_name}.{last_name}@freedommail.com"
        state = random.choice(locations)
        home_ip = generate_random_ip()
        subscription_type = random.choice(subscription_types)

        user = User(
            id=i,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            birthdate=birthdate,
            phone_number=phone_number,
            email=email,
            state=state,
            home_ip_address=home_ip,
            subscription_type=subscription_type,
        )

        session.add(user)

    session.commit()

    for user_id in range(num_users):
        past_movies = (
            session.query(Movie).filter(Movie.release_date < date.today()).all()
        )
        for _ in range(random.randint(5, 10)):
            watched_movie = random.choice(past_movies)
            delta = (date.today() - watched_movie.release_date).days
            random_days = random.randint(0, delta)
            random_timestamp = watched_movie.release_date + timedelta(days=random_days)

            view_history_entry = ViewHistory(
                user_id=user_id,
                movie_id=watched_movie.id,
                view_timestamp=random_timestamp,
                device=random.choice(devices),
                location=random.choice(locations),
            )

            # Add the record to the session and commit
            session.add(view_history_entry)

        # Insert random search history for the user
        for _ in range(random.randint(10, 20)):  # Random number of views
            timestamp = datetime.today() - timedelta(
                days=random.randint(0, 365 * 2)
            )  # last two years

            search_history_entry = SearchHistory(
                user_id=user_id,
                search_query=random.choice(adjectives + nouns + genres),
                search_timestamp=timestamp,
                device=random.choice(devices),
                location=random.choice(locations),
            )

            # Add the record to the session and commit
            session.add(search_history_entry)

    session.commit()

    # Close the session
    session.close()
