import pandas as pd
import requests
import datetime
import os


# creat function to be used in other python files
def return_df(TOKEN):
    input_variables = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN),
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=2)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # download all songs you have listened to after yesterday which means in the last 24 hrs.
    r = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?after={time}".format(
            time=yesterday_unix_timestamp
        ),
        headers=input_variables,
    )

    data = r.json()
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # extracting only the relevant bits of data from the json object
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    # prepare a dictionary in order to turn it into pandas dataframe
    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps,
    }
    song_df = pd.DataFrame(song_dict)
    return song_df
