import os
import argparse
import re
from pytube.__main__ import YouTube
import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from moviepy.editor import VideoFileClip


def main():

    parser = argparse.ArgumentParser(description="Input the link that you want to download. Has some flags thay modify behavior.")

    parser.add_argument("-s", action="store_true", dest="silence", help="silences the prompts for title and artist")
    parser.add_argument("link", type=str, help="yt link that you want to download")
    

    ns = parser.parse_args()

    # Getting the .mp4 file from yt

    yt = YouTube(ns.link)

    stream = yt.streams.filter(
        only_audio=False, audio_codec="mp4a.40.2").order_by("abr").desc()

    title = stream[0].title

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

    if "remix" in title or "Remix" in title:
        rem = re.findall("[a-z]* remix", title, re.IGNORECASE)[0]
        track = f"{track} - {rem}"
        track = track.strip()

    if not ns.silence:
        track_yea_or_nay = input(f"Is the song's title \"{track}\"? (y/n)")

        if track_yea_or_nay.lower() != "y":
            track = input("What is the song's title?")

        artist_yea_or_nay = input(f"Is the song's artist \"{artist}\"? (y/n)")

        if artist_yea_or_nay.lower() != "y":
            artist = input("What is the song's artist?")

    print("Downloading...")

    stream[0].download(filename=f"{track}.mp4")

    # Converting file from .mp4 to .mp3

    video = VideoFileClip(f"{track}.mp4")

    audio = video.audio

    audio.write_audiofile(f"{track}.mp3")

    video.close()

    audio.close()

    # Applying APIC ID3 tag

    img_data = requests.get(yt.thumbnail_url).content

    audio = ID3(f"{track}.mp3")

    audio.add(APIC(mime="jpg", data=img_data, type=3))

    audio.save(f"{track}.mp3")

    # Applying easy tags

    audio_e = EasyID3(f"{track}.mp3")

    audio_e["artist"] = artist

    audio_e["title"] = track

    audio_e.save()

    os.remove(f"{track}.mp4")

    # windows likes to keep the thumbnail file around after downloading
    for root, dir, files in os.walk("."):
        if "Folder.jpg" in files:
            os.remove("Folder.jpg")
        if "AlbumArtSmall.jpg" in files:
            os.remove("AlbumArtSmall.jpg")


if __name__ == "__main__":
    main()
