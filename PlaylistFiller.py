from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# KVRX Playlist Filler
# Make sure you download the latest "chromedriver" from the web
# Then add it to your computers PATH

def fill_out_song_info(driver, track_name, album_name, artist, track_index):
    base_track_id = "edit-field-playlist-tracks-und-{}-{}"
    
    track_name_form = driver.find_element_by_id(base_track_id.format(i, "track-name"))
    track_name_form.send_keys(track_name)

    album_name_form = driver.find_element_by_id(base_track_id.format(i, "album-name"))
    album_name_form.send_keys(album_name)

    artist_form = driver.find_element_by_id(base_track_id.format(i, "artist"))
    artist_form.send_keys(artist)

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

if __name__ == "__main__":
    driver = webdriver.Chrome()

    login_to_kvrx(driver, "your_kvrx_username", "your_kvrx_password")

    spotify_playlist = spotify.get_playlist("playlist_url")
    create_playlist(spotify_playlist)

    driver.close()

