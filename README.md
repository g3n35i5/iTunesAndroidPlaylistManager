# iTunesAndroidPlaylistManager

I wrote this parser to import playlists exported from iTunes into the app
"Rocket Player" on my Android smartphone.

## Setup

First, the paths to the respective directories on Windows and Android must
be set in the `PlaylistManager.py` file. An example would be

```
WINDOWS_MUSIC_PATH = 'E:\Music\'
```

for the windows path and

```
ANDROID_MUSIC_PATH = '/storage/sdcard/music/'
```
for the path on the smartphone.

## Usage

Copy the exported playlists to the playlist folder in this project. The format
must correspond to that of the file `example. m3u`. By the way: You don't have
to delete this file, it will be ignored by the program.

Make sure the Android tools are installed on your computer and an adb server is
running in root mode. This is necessary because the app directories on the
smartphone can only be used by root users.

Furthermore, the ADB connection on the smartphone must first be confirmed and
allowed.

Start the program with the command

```bash
$ python3 PlaylistManager.py
```
