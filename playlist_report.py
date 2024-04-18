'''
@title: playlist_report
@author:jtrebilcock
@date: 4/15/2024

Usage: write out a simple txt report of songs with name, arts, and added date
'''

import spotipy, datetime

def auth_me(id, secret, user, redirect):
    '''authorize app to access playlist data'''
    auth_cred = spotipy.SpotifyOAuth(client_id=id, 
                                     client_secret = secret, 
                                     redirect_uri =redirect, 
                                     scope = 'user-library-read playlist-modify-private', 
                                     username= user)
    
    code = auth_cred.get_auth_response()
    token = auth_cred.get_access_token(code, as_dict=False)
    return spotipy.Spotify(token)

def get_playlist_id(sp, user_id, playlist_search):
    '''get playlist id using its name'''
    playlist_of_interest = [playlist for playlist in sp.user_playlists(user_id)['items'] if playlist['name'] ==playlist_search][0]
    return playlist_of_interest['id']
    
def get_data(song):
    '''extract data from a track dict'''
    song_name = song['track']['name']
    #order artists
    artists = [band['name'] for band in song['track']['artists']]
    artist_value = ', '.join(sorted(artists))
    #date formatting
    date = datetime.datetime.strptime(song['added_at'], '%Y-%m-%dT%H:%M:%SZ')
    day_added = date.strftime('%m/%d/%Y')
    
    return {song['track']['id']:{'name': song_name, 'artists': artist_value, 'added_date':day_added}}

def write_report(playlist_song_data, out_loc):
    '''write out a simple txt report of songs with name, arts, and added date'''
    f = open(out_loc, 'w', encoding='utf-8')
    for data in playlist_song_data.values():
        f.write(f'"{data['name']}"    {data['artists']}   {data['added_date']}\n')

def main():
    #perameters
    my_client_id = ''
    secret = ''
    user = ''
    app_redirect = r''
    playlist_search = ''
    output = r''
    
    #authorized
    my_spotify = auth_me(my_client_id, secret, user, app_redirect)
    
    #access playlists and find the one you are interested in.
    playlist_of_interest = get_playlist_id(my_spotify, user, playlist_search)
    playlist =  my_spotify.user_playlist_tracks(user, playlist_of_interest)   
    tracks = playlist['items']
    
    #spotipy limits reults to 100 at a time so use next method to get next pages and extend list of track dicts
    while playlist['next']:
        playlist = my_spotify.next(playlist)
        tracks.extend(playlist['items'])
        
    #hold output to write report
    results = {}    
        
    #get song data we care about
    for song in tracks:
        results.update(get_data(song))
        
    #write out a simple txt report in chosen location
    write_report(results, output)
    
if __name__ == '__main__':
    main()
