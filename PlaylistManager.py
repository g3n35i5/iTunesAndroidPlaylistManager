#!/usr/bin/env python3

import os
import sqlite3
import sys
_path = os.path.dirname(os.path.abspath(__file__)) + '/'


# Set variables
APP_NAME = 'com.jrtstudio.AnotherMusicPlayer'
ANDROID_DB_PATH = '/data/data/{}/files/blob3.blob'.format(APP_NAME)
PLAYLIST_PATH = _path + 'playlists'
WINDOWS_MUSIC_PATH = 'PATH_TO_YOUR_WINDOWS_MUSIC_DIRECTORY'
ANDROID_MUSIC_PATH = 'PATH_TO_YOUR_ANDROID_MUSIC_DIRECTORY'


# Parser intern playlist class
class Playlist():
    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.members = []

    def addMember(self, song):
        self.members.append(song)

    def __repr__(self):
        rep = '<Playlist {}, Name: {}, Members: {}>'
        return rep.format(self.id, self.name, len(self.members))


# Parser intern playlistmember class
class PlaylistMember():
    def __init__(self, path, playlistID):
        self.path = path
        self.playlistID = playlistID

    def __repr__(self):
        rep = '<PlaylistMember, path: {}, playlistID: {}>'
        return rep.format(self.path, self.playlistID)


# Dictionary,  in which parser internally the playlists are generated
_playlists = {}

for filename in os.listdir(PLAYLIST_PATH):
    if filename.endswith(".m3u") and filename != 'example.m3u':
        with open(os.path.join(PLAYLIST_PATH, filename), 'r') as _f:
            _playlists[filename.replace('.m3u', '')] = _f.readlines()

try:
    os.system('adb pull {} androidDatabase.db'.format(ANDROID_DB_PATH))
except:
    sys.exit("Can not copy database to current folder.")

con = sqlite3.connect('androidDatabase.db')
cur = con.cursor()

# Wipe all existing playlists from android database
cur.execute('DELETE FROM playlists;')
cur.execute('DELETE FROM playlistsMembers;')

playlists = []

playlistNumber = 1

for playlist in _playlists:
    currentPlaylist = Playlist(id=playlistNumber, name=playlist)
    for line in _playlists[playlist]:
        if not line.startswith('#'):
            line = line.strip()
            line = line.replace('\\', '/')
            line = line.replace(WINDOWS_MUSIC_PATH, ANDROID_MUSIC_PATH)

            member = PlaylistMember(path=line, playlistID=playlistNumber)
            currentPlaylist.addMember(member)

    playlists.append(currentPlaylist)
    playlistNumber += 1

for playlist in playlists:
    print('Creating Playlist "{}"'.format(playlist.name))

    cur.execute('INSERT INTO playlists '
                '(_fileDateModified, _fileSize, _name, _file) '
                'VALUES(?,?,?,?);', (0, 0, playlist.name, None)
                )

    position = 0
    for member in playlist.members:
        cur.execute('INSERT INTO playlistsMembers '
                    '(_path, _id, _position) VALUES(?,?,?);',
                    (member.path, member.playlistID, position)
                    )

        position += 1
    print('\tAdded {} songs'.format(position))


con.commit()

try:
    os.system('adb push androidDatabase.db {}'.format(ANDROID_DB_PATH))
    os.system('adb shell am force-stop {}'.format(APP_NAME))
    os.system('adb shell am start {}'.format(APP_NAME))
except:
    sys.exit("Can not copy database to Android device.")
