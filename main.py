import os
from pytube.__main__ import YouTube
import requests
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from moviepy.editor import VideoFileClip


def main():

    # Getting the .mp4 file from yt

    yt = YouTube("https://www.youtube.com/watch?v=MY8Es1ENZ2E")

    stream = yt.streams.filter(
        only_audio=False, audio_codec="mp4a.40.2").order_by("abr").desc()

    title = stream[0].title.split(" ")

    artist = title[0]

    track = title[2]

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


if __name__ == "__main__":
    main()
