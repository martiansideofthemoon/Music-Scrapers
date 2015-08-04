Simple command line scrapers to download music,get song details and get lyrics.
Supply song and artist names in command line arguments.

USAGE :- 

<b>Mp3Skull Scrape</b><br>
./download.py [FLAGS] SEARCH_QUERY<br>
-r, --remix		If the song is a remix.<br>
-c, --cover		If the song is a cover.<br>
-s, --short		If the song length is under 90 seconds.<br>
download.py also uses song_details.py to put the required metadata.

./song_details.py [FLAGS] SEARCH_QUERY<br>

<b>Automatic Lyrics Finder</b><br>
./lyricsfinder SEARCH_QUERY<br>

Integration with Rhythmbox coming up...
