Through my experience in DJ'ing, I have found that energy and danceabillity levels have been more significant than the genre or beats-per-minute of a song. 
Therefore, instead of the standard approach of organising music libraries by genre or BPM, I wanted to organise mine by energy and danceability levels.
This could be done manually by sorting each song individually (3000+ songs) but I decided to leverage the Spotify API to automate this, which assigns energy and danceability levels to all songs in the Spotify database.
K-means clustering is then used to group songs with similar energy and danceabiity levels together, with the program assigning the songs to new Spotify playlists accordingly, based on how they were grouped.
