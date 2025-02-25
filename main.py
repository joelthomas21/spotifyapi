import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Getting spotify api
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id= "INSERT CLIENT ID",
        client_secret= "INSERT CLIENT SECRET",
        show_dialog=True,
        cache_path="token.txt",
        username="INSERT SPOTIFY USERNAME",
    )
)
user_id = sp.current_user()["id"]

# Getting the song data

all_songs_playlist = sp.playlist_tracks(playlist_id="INSERT A PLAYLIST OF ALL THE SONGS TO BE ANALYSED")


#TODO: get the track ids from all_songs_playlist and pass those into sp.audio_features
#print(all_songs_playlist['items'])
track_uris = []
for item in all_songs_playlist['items']:
    track_uris.append(item['track']['uri'])


audio_features = sp.audio_features(tracks=track_uris)
features_dict = {}

track_names = []
for item in all_songs_playlist['items']:
    track_name = (item['track']['name'])
    track_names.append(track_name)

track_no = 0
for track in audio_features:
    dnce = track['danceability']
    nrg = track['energy']
    uri = track_uris[track_no]
    features_dict[track_names[track_no]] = {'danceability': dnce, 'energy': nrg, 'uri':uri}

    track_no += 1

#CLUSTERING THE SONGS BY ENERGY AND DANCEABILITY

# Extract danceability and energy data into a DataFrame
song_names = list(features_dict.keys())
danceability = [features_dict[song]['danceability'] for song in song_names]
energy = [features_dict[song]['energy'] for song in song_names]
ur = [features_dict[song]['uri'] for song in song_names]

data = pd.DataFrame({
    'track title': song_names,
    'danceability': danceability,
    'energy': energy,
})


# Preparing the data for k-means clustering (only the features)
X = data[['danceability', 'energy']]


# Defining the number of clusters
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans.fit(X)

# Getting the cluster labels and adding them to the dataframe
data['cluster'] = kmeans.labels_

# Visualising the clusters
plt.figure(figsize=(8, 6))
plt.scatter(data['danceability'], data['energy'], c=data['cluster'], cmap='viridis')
plt.xlabel('Danceability')
plt.ylabel('Energy')
plt.title('K-means Clustering my Music Library by Danceability and Energy')

#print(data)
for index, row in data.iterrows():
    cluster = f"{row['cluster']}"
    features_dict[f"{row['track title']}"].update({'cluster': cluster})
print(features_dict)

plt.show()

low_nrg_hi_dnce0 = []
hi_nrg_hi_dnce1 = []
low_nrg_low_dnce2 = []
hi_nrg_low_dnce3 = []

#print(features_dict)
for song in features_dict.values():
    (song_cluster) = str(song['cluster'])
    song_uri = song['uri']

    print(song_cluster)

    if song_cluster == '0':
        low_nrg_hi_dnce0.append(song_uri)


    elif song_cluster == '1':
        hi_nrg_hi_dnce1.append(song_uri)
    elif song_cluster == '2':
        low_nrg_low_dnce2.append(song_uri)
    else:
        hi_nrg_low_dnce3.append(song_uri)


low_hi = sp.user_playlist_create(user=user_id,name='low_nrg_hi_dnce', public=False)
hi_hi = sp.user_playlist_create(user=user_id,name='hi_nrg_hi_dnce', public=False)
low_low = sp.user_playlist_create(user=user_id,name='low_nrg_low_dnce', public=False)
hi_low = sp.user_playlist_create(user=user_id,name='hi_nrg_low_dnce', public=False)
# print(low_hi)

sp.playlist_add_items(playlist_id=low_hi['id'], items=low_nrg_hi_dnce0)
sp.playlist_add_items(playlist_id=hi_hi['id'], items=hi_nrg_hi_dnce1)
sp.playlist_add_items(playlist_id=low_low['id'], items=low_nrg_low_dnce2)
sp.playlist_add_items(playlist_id=hi_low['id'], items=hi_nrg_low_dnce3)
