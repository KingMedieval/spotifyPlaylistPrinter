import requests
import base64
import json
import math


# generates spotify api token
def tokenGen(spotify_client_ID, spotify_client_secret):
    # the client id and the client secret is spliced in
    # spotify_client_ID:spotify_client_secret format
    clientIDSecret = spotify_client_ID + ':' + spotify_client_secret

    # the spliced string is converted to base64
    clientIDSecret_bytes = clientIDSecret.encode('ascii')
    base64_bytes = base64.b64encode(clientIDSecret_bytes)
    base64_str = base64_bytes.decode('ascii')

    # declares the variables for the requests to API including URL of the
    # API, Authorization encoded in base64, and the type of grant
    # client_credential is token generation without user login thru spotify
    url = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': 'Basic ' + base64_str}
    data = {'grant_type': 'client_credentials'}

    # sends a HTTP POST request to the Spotify Web API with the variables
    r = requests.post(url, headers=headers, data=data)

    # if there is api error or client info is wrong, outputs error code 1000
    # status code 200 means OK (success)
    if not r.status_code == 200:
        errCode = 1000
        token = ' '
        return errCode, token

    # response is recorded to text
    text = r.text

    # respose is converted to JSON (dict) data type then the access_token is extracted
    text = json.loads(text)
    token = text["access_token"]
    errCode = 0

    return errCode, token


# Parses playlist information from the Spotify API
def getPlaylistInfo(playlistURL, token):
    # checks if the link is a valid link by comparing to a template
    playlistURLTemplate = 'https://open.spotify.com/playlist/'
    if playlistURLTemplate in playlistURL:
        # if template is in the URL, countinues on
        errCode = 0

        # cuts the playlist ID (Spotify URI) from the URL
        playlistID = playlistURL[34:56]

        # declares the variables for the requests to the API for the playlist info
        url = 'https://api.spotify.com/v1/playlists/' + playlistID
        headers = {'Authorization': 'Bearer ' + token}

        # sends a HTTP GET request to the Spotify Web API with the variables
        r = requests.get(url, headers=headers)

        # if there is api error, outputs error code 1001
        # status code 200 means OK (success)
        if not r.status_code == 200:
            errCode = 1001
            playlistInfo = ' '
            return errCode, playlistInfo, playlistID

        # response is recorded to text
        text = r.text

        # respose is converted to JSON (dict) data type
        playlistInfo = json.loads(text)

    else:
        # if it does not fit the template, it gives out an error and exits function
        errCode = 2000
        playlistInfo = ' '
        playlistID = ' '
    return errCode, playlistInfo, playlistID


# Parses tracklist and track information from Spotify API
# ***Due to limiations, Spotify only allows parsing 100 songs at a time and
#   and the program runs multiple times to compensate for the limitation***
def getTracks(playlistID, noTracks, token):
    # initiate variables
    tracklist = []
    errCode = 0
    i = 0
    # set the number of times the loop has to run
    run = math.ceil(noTracks / 100)

    while i < run:
        offset = i * 100
        # declares the variables for the requests to the API for the playlist info
        url = 'https://api.spotify.com/v1/playlists/' + playlistID + '/tracks?offset=' + str(offset)
        headers = {'Authorization': 'Bearer ' + token}

        # sends a HTTP GET request to the Spotify Web API with the variables
        r = requests.get(url, headers=headers)

        # if there is api error, outputs error code 1001
        # status code 200 means OK (success)
        if not r.status_code == 200:
            errCode = 1002
            return errCode, tracklist

        # response is recorded to text
        text = r.text

        # respose is converted to JSON (dict) data type and appended to the tracklist list
        tracklist.append(json.loads(text))

        i = i + 1
    return errCode, tracklist
