from pytube.__main__ import YouTube
import requests
import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import re
from moviepy.editor import VideoFileClip

def main():
    yt = YouTube("https://www.youtube.com/watch?v=MY8Es1ENZ2E")
    
    stream = yt.streams.filter(only_audio=False, audio_codec="mp4a.40.2").order_by("abr").desc()

    artist = re.findall("^[a-z]*", stream[0].title, re.IGNORECASE)[0]

    stream[0].download(filename=f"{artist}.mp4")

    video = VideoFileClip(f"{artist}.mp4")

    audio = video.audio

    audio.write_audiofile(f"{artist}.mp3")

    video.close()

    audio.close()

    # img_data = requests.get(yt.thumbnail_url).content

    audio = EasyID3(f"{artist}.mp3")

    audio["artist"] = artist

    

    audio.save()





if __name__ == "__main__":
    main()