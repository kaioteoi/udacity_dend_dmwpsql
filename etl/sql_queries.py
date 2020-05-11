# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE songplays (
    timestamp DOUBLE PRECISION,
    user_id BIGINT,
    level TEXT,
    song_id TEXT,
    artist_id TEXT,
    session_id BIGINT,
    location TEXT,
    user_agent TEXT
);
""")

user_table_create = ("""
CREATE TABLE users (
    id BIGINT,
    first_name TEXT,
    last_name TEXT,
    gender CHAR(1),
    level TEXT
)
""")

song_table_create = ("""
CREATE TABLE songs (
    id TEXT,
    title TEXT,
    artist_id TEXT,
    year SMALLINT,
    duration DOUBLE PRECISION
);
""")

artist_table_create = ("""
CREATE TABLE artists (
    id TEXT,
    name TEXT NOT NULL,
    location TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);
""")

time_table_create = ("""
CREATE TABLE time (
    timestamp DOUBLE PRECISION,
    hour SMALLINT,
    day SMALLINT,
    week_of_year SMALLINT,
    month SMALLINT,
    year SMALLINT,
    weekday SMALLINT
);
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (timestamp, user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO users (id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s)
""")

song_table_insert = ("""
INSERT INTO songs (id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s)
""")

artist_table_insert = ("""
INSERT INTO artists (id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s)
""")


time_table_insert = ("""
INSERT INTO time (timestamp, hour, day, week_of_year, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

song_select = ("""
SELECT songs.id, songs.artist_id
FROM songs
JOIN artists ON artists.id = songs.artist_id
WHERE songs.title = %s
AND artists.name = %s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]