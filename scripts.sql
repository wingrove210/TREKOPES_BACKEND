CREATE TABLE tracks (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    artist VARCHAR NOT NULL,
    file_url VARCHAR,
    image_url VARCHAR
);

CREATE TABLE news (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    content TEXT NOT NULL,
    image_url VARCHAR,
    published_at TIMESTAMP
);
