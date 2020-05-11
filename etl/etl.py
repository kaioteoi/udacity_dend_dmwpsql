import os
import glob
from datetime import datetime

import psycopg2
import pandas as pd

from sql_queries import *
from create_tables import main as bootstrap

_NEXT_SONG_ACTION = "NextSong"
_SONG_COLUMNS = ["song_id", "title", "artist_id", "year", "duration"]
_ARTIST_COLUMNS = ["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]
_TIME_COLUMNS = ["timestamp", "hour", "day", "week of year", "month", "year", "weekday"]
_USER_COLUMNS = ["userId", "firstName", "lastName", "gender", "level"]


def _df_unique_values_list(df, columns):
    return df[columns].values.tolist()[0]


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = _df_unique_values_list(df, _SONG_COLUMNS)
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = _df_unique_values_list(df, _ARTIST_COLUMNS)
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == _NEXT_SONG_ACTION]

    # convert timestamp column to datetime
    t = (df.ts/1000).map(datetime.fromtimestamp).dt
    
    # insert time data records
    time_data = [df.ts, t.hour, t.day, t.weekofyear, t.month, t.year, t.weekday]
    time_df = pd.DataFrame(
        dict(list(zip(*[_TIME_COLUMNS, time_data])))
    )

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_id_null_holder = ('' if df.userId.dtype != 'int64' else 0)
    filter_blank_user_id = df.userId != user_id_null_holder
    user_df = df.loc[filter_blank_user_id][_USER_COLUMNS].drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.replace({'userId': {user_id_null_holder: None}}).iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist))
        results = cur.fetchone()
        
        songid, artistid = results or (None, None)

        # insert songplay record
        songplay_data = (
            row.ts,
            row.userId,
            row.level,
            songid,
            artistid,
            row.sessionId,
            row.location,
            row.userAgent,
        )
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    bootstrap()
    
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()