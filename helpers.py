import argparse
import re
import requests
import os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from moviepy.audio.io.AudioFileClip import AudioFileClip


def command_line_parser(*args):
    # command arguments
    args = args[0]
    if args["exe"]:
        return
    parser = argparse.ArgumentParser(
        description="Input the link that you want to download. Has some flags thay modify behavior."
    )
    parser.add_argument(
        "-s",
        action="store_true",
        dest="silence",
        help="silences the prompts for title and artist",
    )
    parser.add_argument("link", type=str, help="yt link that you want to download")
    parser.add_argument(
        "-p",
        action="store_true",
        dest="playlist",
        help="explicitly enable playlist mode",
    )
    return parser.parse_args()


def parse_title(title):
    """looks through the title of the video for the author & song name.
    will try to find remix name and append that to the title as well"""
    artist = ""
    track = ""

    if title[0] == "[":
        while title[0] != "-":
            title = title[1:]
        title = title[1:]
        title = title.strip()

    for char in title:
        if char in "-":
            break
        artist = artist + char

    broken = False

    for char in title:
        if char in "-":
            broken = True
            continue
        if not broken:
            continue
        else:
            if char in "[(":
                break
            else:
                track = track + char

    artist = artist.strip()
    track = track.strip()

    try:
        if "remix" in title or "Remix" in title:
            rem = re.findall("[a-z]* remix", title, re.IGNORECASE)[0]
            track = f"{track} - {rem}"
            track = track.strip()
    except IndexError:
        # in case remix is by itself in title
        pass

    return {"artist": artist, "track": track}


def song_questionare(track_info, ns):
    """uses info from parse_track to question the user about their song.
    replaces info from parse_track upon user request"""
    track = track_info["track"]
    artist = track_info["artist"]
    if not ns:
        return {"artist": artist, "track": track}
    if not ns.silence:
        track_yea_or_nay = input(f'Is the song\'s title "{track}"? (y/n)')

        if track_yea_or_nay.lower() != "y":
            track = input("What is the song's title?")

        try:
            artist_yea_or_nay = input(f'Is the song\'s artist "{artist}"? (y/n)')
        except UnicodeEncodeError:
            artist = input("What is the song's artist?")
        else:
            if artist_yea_or_nay.lower() != "y":
                artist = input("What is the song's artist?")

    return {"artist": artist, "track": track}


def mp4_to_mp3(track):
    """converts .mp4 videos to .mp3 files.
    doesn't work with .mp4 audio only files"""
    audio = AudioFileClip(f"{track}.mp4")
    audio.write_audiofile(f"{track}.mp3")
    audio.close()


def apply_apic(track, thumbnail_url):
    """gets the video's thumbnail from yt and applies it to
    the audio file as an APIC id3 tag. img_data has to be byte string"""
    img_data = requests.get(thumbnail_url).content
    audio = ID3(f"{track}.mp3")
    audio.add(APIC(mime="jpg", data=img_data, type=3))
    audio.save(f"{track}.mp3")


def apply_id3(track_info):
    """adds artist and title to id3 tags"""
    track = track_info["track"]
    artist = track_info["artist"]

    audio_e = EasyID3(f"{track}.mp3")
    audio_e["artist"] = artist
    audio_e["title"] = track
    audio_e.save()


def single_song_exe_save(track_info):
    mp4_to_mp3(track_info["track"])

    apply_apic(track_info["track"], track_info["url"])
    apply_id3(track_info)

    os.remove(f"{track_info['track']}.mp4")

    os.rename(
        f"{track_info['track']}.mp3", f"{track_info['dir']}\{track_info['track']}.mp3"
    )
