'''
===============================================================================
ENGR 133 Fa 2020

Assignment Information
	Assignment:     Individual Project
	Author:         Dojun, Tomo, tshimada@purdue.edu
	Team ID:        LC1-30 (e.g. LC1-14 for section 1 team 14)

Contributors:       Name, login@purdue [repeat as needed]
	My contributor(s) helped me:
	[] understand the assignment expectations without
		telling me how they will approach it.
	[] understand different ways to think about a solution
		without helping me plan my solution.
	[] think through the meaning of a specific error or
		bug present in my code without looking at my code.
	Note that if you helped somebody else with their code, you
	have to list that person as a contributor here as well.
===============================================================================
'''
import sys
import math
import WebAPIFunction as API


# organizes tracklist information
def organizePlaylistTrackInfo(tracklist, offset):
    # initialize variables
    i = 0
    j = 0
    # song info in order [track number, title, artist, album, duration, release date]
    song = [[0, 0, 0, 0, 0, 0] for x in range(len(tracklist['items']))]

    # repeat for the number indices in the list
    while i < len(tracklist['items']):
        # initialize variables (reset each loop)
        artists = []
        durMinSec = [0, 0]

        # track number (if it runs multiple times, it will add offset to the number)
        song[i][0] = (i + 1) + (offset * 100)
        # track name
        song[i][1] = tracklist['items'][i]['track']['name']
        # artists
        for j in range(len(tracklist['items'][i]['track']['artists'])):
            artists.append(tracklist['items'][i]['track']['artists'][j]['name'])
            j = j + 1
        song[i][2] = ', '.join(artists)
        # album name
        song[i][3] = tracklist['items'][i]['track']['album']['name']
        # song duration (converts from ms to m:s format)
        duration = tracklist['items'][i]['track']['duration_ms'] / 1000
        durMinSec[0] = str(math.floor(duration / 60))
        durMinSec[1] = str(round(duration % 60))
        if round(duration % 60) < 10:
            durMinSec[1] = '0' + str(round(duration % 60))
        else:
            durMinSec[1] = str(round(duration % 60))
        song[i][4] = ':'.join(durMinSec)
        # song/album release date or year
        song[i][5] = tracklist['items'][i]['track']['album']['release_date']
        i = i + 1
    return song


########################
# START OF MAIN FUNCTION#
########################

print('BEFORE USING THE PROGRAM, PLEASE CHANGE THE CILENT ID AND CLIENT SECRET ON LINES 78 AND 80')

'''
CHANGE THE SPOTIFY CLIENT ID AND SECRET BEFORE USING THE PROGRAM
DUE TO TERMS OF SERVICE AND SECURITY, IT IS NOT ALLOWED TO SHARE THE SPOTIFY CLIENT ID AND SECRET
THIS CAN BE OBTAINED BY FOLLOWING THE MANUAL ON THE REPORT
'''
# spotify_client_ID = input('Enter your Spotify Client ID: ')
spotify_client_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
# spotify_client_secret = input('Enter your Spotify Client Secret: ')
spotify_client_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# runs tokenGen function
errCode, token = API.tokenGen(spotify_client_ID, spotify_client_secret)

# checks for an error code if true, code exits
if errCode == 1000:
    print("ERROR 1000: Spotify Web API Error or Incorrect Client ID/Secret")
    sys.exit()

# input playlistURL
playlistURL = input('Enter playlist URL: ')

# runs getPlaylistInfo function
errCode, playlistInfo, playlistID = API.getPlaylistInfo(playlistURL, token)

# checks for an error code if true, code exits
if errCode == 1001:
    print("ERROR 1001: Spotify Web API Error")
    sys.exit()
elif errCode == 2000:
    print(
        "ERROR 2000: Incorrect playlist URL format (correct format https://open.spotify.com/playlist/XXXXXXXXXXXXXXXXXXXXXX?si=XXXXXXXXXXXXXXXXXXXXXX)")
    sys.exit()

# gets the number of tracks
noTracks = playlistInfo['tracks']['total']

# runs getTracks function
errCode, tracklist = API.getTracks(playlistID, noTracks, token)

# checks for an error code if true, code exits
if errCode == 1002:
    print("ERROR 1001: Spotify Web API Error getting tracklist")
    sys.exit()

# declares variables
song = []
i = 0

# set the number of times the loop has to run
run = math.ceil(noTracks / 100)

while i < run:
    # runs organizePlaylistTrackInfo per 100 songs and appends to the song list
    song.append(organizePlaylistTrackInfo(tracklist[i], i))
    i = i + 1

# title of the playlist, description, and the creator of the playlist is stored to a variable
title = playlistInfo['name']
desc = playlistInfo['description']
creator = playlistInfo['owner']['display_name']

outputFileName = title + '_tracklist.txt'

# writes to an external file as a text (.txt) file in a tabular format
with open(outputFileName, "w") as f:
    f.write(title + '\n' + desc + '\nCreated by ' + creator + '\n' + str(noTracks) + ' songs\n\n')
    f.write("{:<7} {:<60} {:<60} {:<60} {:<10} {:<10}\n".format('Song #.', 'Title', 'Artists', 'Album', 'Duration',
                                                                'Release Date'))
    for j in range(len(song)):
        for k in range(len(song[j])):
            f.write("{:<7} {:<60} {:<60} {:<60} {:<10} {:<10}\n".format(song[j][k][0], song[j][k][1], song[j][k][2],
                                                                        song[j][k][3], song[j][k][4], song[j][k][5]))

