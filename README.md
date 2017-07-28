# KVRX_Playlist_Filler
Automatically fill KVRX website playlists

If you're running this for development/testing/curiosity you need python3 and you need to download selenium(pip install selenium) and spotipy(pip install spotipy). You will also need to put the latest [chromedriver](https://chromedriver.storage.googleapis.com/index.html?path=2.31/) on your PATH. 

I'm working on exporting this project to be run as a standalone application on Windows/Linux/Mac

I'm not adding support for super old/weird computers or anything, I'm mainly just making this work so it can run normally on the KVRX booth machine(Mac). And you should not ask me for any more features/automation because then I'm just recreating the website. If you want more features you should add them yourself and submit a pull request. I will add more features as I see fit. 
Also getting playlist stuff from Youtube might happen, but we'll see. 

I'll probably also add a feature to allow you to specify a "playlist" file that looks like this:

  album id - track name - album name - artist - album label   
  ...    
  last album id - last track name - last album name - last artist - last album label  


It may be the case that the user must install chromedriver and specify the path when the application starts(only once), but that's pretty easy to do for both me and the user. 

Instructions:
Navigate to your spotify playlist on the spotify app
![Spotify Playlist](http://i.imgur.com/IDUXcSW.png)

click the ellipsis under the playlist name to get the dropdown
![Playlist ellipsis](http://i.imgur.com/MkkAKBz.png)

select 'Share' and click 'URI'
![Playlist uri](http://i.imgur.com/aPBdQOx.png)

This will copy the 'Playlist URI' to your clipboard, this contains a number version of your playlist and username

Run the playlist filler and you will see a dialog box like this:
![Dialog box](http://i.imgur.com/ItiD70o.png)

Paste the URI you copied into the box, along with the playlist title, date, and show name, then hit submit, it will then open up a browser and fill in all of the tracks(the browser will be the one that says 'Chrome is being controlled by automated test software'), you can then change the playlist description after it is created. 
