import json

import requests
from Google import Create_Service
import pandas as pd

from exceptions import ResponseException
from secrets import client_id, client_secret, spotify_user_id, spotify_token

class Spotify2YouTube:

  def __init__(self):
    self.spotify_access_token = self.get_spotify_access_token()
    self.list_of_tracks = self.get_playlist()
    print(self.list_of_tracks)
    self.playlist_target = 'PL9ZZHYwJcwmS5Ma_zRzDSxl2uiJn8O02y'
    self.youtube_client = self.get_youtube_client()
    # self.create_youtube_playlist()

  def get_youtube_client(self):
    CLIENT_SECRET_FILE  =  'client_secrets.json'
    API_NAME  =  'youtube'
    API_VERSION  =  'v3'
    SCOPES  = ['https://www.googleapis.com/auth/youtube']

    return Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

  def create_youtube_playlist(self):
    video_ids = []
    for track in self.list_of_tracks:
      print(track["name"] + " by " + track["artist"] + " official music video")
      response = self.youtube_client.search().list(
        part='snippet',
        order='viewCount',
        q=track["name"] + " by " + track["artist"] + " official music video",
        type='video',
        maxResults=5
      ).execute()
      items = response["items"]
      video_ids.append(items[0]["id"]["videoId"])

    for val in video_ids:
      print(val)

    for video_id in video_ids:    
      request_body = {
          'snippet': {
              'playlistId': self.playlist_target,
              'resourceId': {
                  'kind': 'youtube#video',
                  'videoId': video_id
              }
          }
      }

      self.youtube_client.playlistItems().insert(
          part='snippet',
          body=request_body
      ).execute()

  def get_spotify_access_token(self):
    query = "https://accounts.spotify.com/api/token"
    response = requests.post(
        query,
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        }
    )
    response_json = response.json()
    return response_json["access_token"]


  # Step 3
  def get_playlist(self):
    query = "https://api.spotify.com/v1/playlists/5wRVLdDqKhuoGPfG6Sc7TI"
    response = requests.get(
        query,
         headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_access_token)
        }
    )
    response_json = response.json()
    list_of_tracks = []
    print(response_json)
    for track in response_json["tracks"]["items"]:

      track_name = track["track"]["name"]
      track_artists = ""
      for artist in track["track"]["artists"]:
        track_artists += artist["name"] + " "

      new_track = {
        "name": "{}".format(track_name),
        "artist": "{}".format(track_artists)
      }

      list_of_tracks.append(new_track)

    # playlist id
    return list_of_tracks

test = Spotify2YouTube()
