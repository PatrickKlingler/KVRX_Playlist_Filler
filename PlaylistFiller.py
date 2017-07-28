from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util as util
import pprint
from tkinter import Tk, Entry, Button, Label, StringVar, W, Text
from time import sleep
import os

pp = pprint.PrettyPrinter(indent=1)
playlist_uri = None


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
    
    track_name_form = driver.find_element_by_id(base_track_id.format(track_index, "track-name"))
    track_name_form.send_keys(track_name)

    album_name_form = driver.find_element_by_id(base_track_id.format(track_index, "album-name"))
    album_name_form.send_keys(album_name)

    artist_form = driver.find_element_by_id(base_track_id.format(track_index, "artist"))
    artist_form.send_keys(artist)

    add_more_button = driver.find_element_by_name("field_playlist_tracks_add_more").click()
    sleep(.5)


def fill_out_playlist(driver, playlist):
    driver.find_element_by_partial_link_text("Create Playlist").click()  

    title_form = driver.find_element_by_id("edit-title")
    title_form.send_keys("Playlist Title")  
    playlist_length = len(playlist['track_names'])
    for i in range(playlist_length):
        #get these from spotify, will be part of a list of playlist track objects or something
        track_name = playlist['track_names'][i]
        album_name = playlist['album_names'][i]
        artist = playlist['artists'][i]
        fill_out_song_info(driver, track_name, album_name, artist, i)

def login_to_kvrx(driver, user_name, pass_word):
    driver.get("http://www.kvrx.org/user")

    username = driver.find_element_by_id("edit-name")
    username.send_keys(user_name)

    password = driver.find_element_by_id("edit-pass")
    password.send_keys(pass_word)

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
    return playlist

def create_playlist(sp, username, playlist_id):
    playlist = {}
    results = sp.user_playlist(username, playlist_id, fields="tracks,next")
    tracks = results['tracks']
    playlist['album_names'] = []
    playlist['artists'] = []
    playlist['track_names'] = []
    playlist = get_information_from_tracks(sp, playlist, tracks)
    return playlist

def parse_playlist_uri(raw_uri):
    raw_uri = raw_uri.split(':')
    return raw_uri[2], raw_uri[4]

def get_playlist_info_from_dialog():
    master = Tk()
    master.title("KVRX Playlist Filler")
    Label(master, text="Playlist URI").grid(row=0)
    Label(master, text="Playlist Title").grid(row=1)
    Label(master, text="Playlist Date").grid(row=2)
    Label(master, text="Show name").grid(row=3)

    playlist_uri = StringVar()
    playlist_title = StringVar()
    playlist_date = StringVar()
    show_name = StringVar()

    playlist_uri_entry = Entry(master, textvariable=playlist_uri)
    playlist_uri_entry.insert(60, 'spotify:user:1270874820:playlist:6pu0ez0zwoeJI5yBK30R3o')

    playlist_title_entry = Entry(master, textvariable=playlist_title)
    playlist_title_entry.insert(60, 'Playlist Title')

    playlist_date_entry = Entry(master, textvariable=playlist_date)
    playlist_date_entry.insert(10, 'MM/DD/YYYY')

    show_name_entry = Entry(master, textvariable=show_name)
    show_name_entry.insert(60, 'The Lab')

    playlist_uri_entry.grid(row=0, column=1)
    playlist_title_entry.grid(row=1, column=1)
    playlist_date_entry.grid(row=2, column=1)
    show_name_entry.grid(row=3, column=1)

    Button(master, text='Quit', command=master.quit).grid(row=4, column=0, sticky=W, pady=4)
    Button(master, text='Submit', command=master.quit).grid(row=4, column=1, sticky=W, pady=4)
    master.mainloop()
    master.destroy()
    return playlist_uri.get(), playlist_title.get(), playlist_date.get(), show_name.get()


if __name__ == "__main__":

    # get playlist uri from user
    playlist_uri, playlist_title, playlist_date, show_name = get_playlist_info_from_dialog()
    username, playlist_id = parse_playlist_uri(playlist_uri)
    print(username, playlist_id, playlist_date, playlist_title, show_name)

    token = util.prompt_for_user_token(username, scope)

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    playlist = create_playlist(sp,username, playlist_id)

    playlist['playlist_title'] = playlist_title
    playlist['playlist_date'] = playlist_date
    playlist['show_name'] = show_name

    try:
        driver = webdriver.Chrome()

        # probably should use an intern account or something, not the actual user's user/pass
        login_to_kvrx(driver, "kvrx username", "kvrx password")

        fill_out_playlist(driver, playlist)
        driver.close()
    except(Exception):
        driver.close()
