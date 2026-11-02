
CREATE TABLE IF NOT EXISTS films (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255),
  director VARCHAR(255)
);

TRUNCATE table films;

INSERT INTO films (title, director) VALUES ('Blade Runner', 'Ridley Scott');
INSERT INTO films (title, director) VALUES ('Gladiator', 'Ridley Scott');
INSERT INTO films (title, director) VALUES ('Inception', 'Christopher Nolan');
INSERT INTO films (title, director) VALUES ('Blue Velvet', 'David Lynch');
