-- Insert data into user table
INSERT INTO user (name, subscription_type) VALUES ('Alice', 'Premium');
INSERT INTO user (name, subscription_type) VALUES ('Bob', 'Basic');

-- Insert data into movie table
INSERT INTO movie (title, genre, release_date, licence_cost, content_expiry) 
VALUES ('Future Blockbuster', 'Sci-Fi', '2025-06-01', 10000, '2026-06-01');
INSERT INTO movie (title, genre, release_date, licence_cost, content_expiry) 
VALUES ('Classic Drama', 'Drama', '2022-04-01', 5000, '2024-04-01');

-- Insert data into watch_history table
INSERT INTO watch_history (user_id, movie_id, watched_on) VALUES (1, 1, '2024-11-01');
INSERT INTO watch_history (user_id, movie_id, watched_on) VALUES (2, 2, '2023-07-15');

-- Insert data into genre table
INSERT INTO genre (name) VALUES ('Sci-Fi');
INSERT INTO genre (name) VALUES ('Drama');

-- Insert data into license_providers table
INSERT INTO license_providers (name, license_fee) VALUES ('License Corp', 5000);
INSERT INTO license_providers (name, license_fee) VALUES ('Media Partners', 3000);