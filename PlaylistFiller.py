from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util as util
import pprint

pp = pprint.PrettyPrinter(indent=1)

# KVRX Playlist Filler
# Make sure you download the latest "chromedriver" from the web
# Then add it to your computers PATH
# All of these clicks may have to be done the "safe" way where we wait
# for the object that it triggers to appear instead of just immediately 
# going to the next thing. But for now it works so we'll worry about it
# when we get there.

scope = 'user-library-read'

def fill_out_song_info(driver, track_name, album_name, artist, track_index):
    base_track_id = "edit-field-playlist-tracks-und-{}-{}"
    
    track_name_form = driver.find_element_by_id(base_track_id.format(i, "track-name"))
    track_name_form.send_keys(track_name)

    album_name_form = driver.find_element_by_id(base_track_id.format(i, "album-name"))
    album_name_form.send_keys(album_name)

    artist_form = driver.find_element_by_id(base_track_id.format(i, "artist"))
    artist_form.send_keys(artist)

    add_more_button = driver.find_element_by_name("field_playlist_tracks_add_more").click()   

def create_playlist(spotify_playlist):
    driver.find_element_by_partial_link_text("Create Playlist").click()  

    title_form = driver.find_element_by_id("edit-title")
    title_form.send_keys("Playlist Title")  
    playlist_length = len(spotify_playlist)
    for i in range(playlist_length):
        #get these from spotify, will be part of a list of playlist track objects or something
        track_name = "super edgy non blacklisted song"
        album_name = "super edgy non blacklisted album"
        artist = "super edgy non blacklisted artist"
        fill_out_song_info(track_name, album_name, artist, i)

def login_to_kvrx(driver, user_name, pass_word):
    driver.get("http://www.kvrx.org/user")

    username = driver.find_element_by_id("edit-name")
    username.send_keys("your_kvrx_username")

    password = driver.find_element_by_id("edit-pass")
    password.send_keys("your_kvrx_password")

    driver.find_element_by_id("edit-submit").click()

def get_track_information(playlist, tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        playlist['album_names'].append(track['album']['name'])
        playlist['artists'].append(track['artists'][0]['name'])
        playlist['track_names'].append(track['name'])
    return playlist

def get_information_from_tracks(sp, playlist, tracks):
    playlist = get_track_information(playlist, tracks)
    while tracks['next']:
        tracks = sp.next(tracks)
        playlist = get_track_information(playlist, tracks)

def create_playlist(sp, username, playlist_id):
    playlist = {}
    results = sp.user_playlist(username, playlist_id, fields="tracks,next")
    tracks = results['tracks']
    playlist['album_names'] = []
    playlist['artists'] = []
    playlist['track_names'] = []
    playlist = get_information_from_tracks(sp, playlist, tracks)

if __name__ == "__main__":
    username = '1270874820'
    playlist_id = '6pu0ez0zwoeJI5yBK30R3o'

    token = util.prompt_for_user_token(username, scope)

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    playlist = create_playlist(sp,username, playlist_id)

    pp.pprint(playlist)

    driver = webdriver.Chrome()

    login_to_kvrx(driver, "your_kvrx_username", "your_kvrx_password")

    spotify_playlist = spotify.get_playlist("playlist_url")
    create_playlist(spotify_playlist)

    driver.close()

