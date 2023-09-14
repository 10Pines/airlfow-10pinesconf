CREATE TABLE IF NOT EXISTS movies (
    id VARCHAR(255) PRIMARY KEY,
    film VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    score INT NOT NULL
);

CREATE ROLE pinesconf WITH SUPERUSER;
