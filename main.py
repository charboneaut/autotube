import os
from pytube.__main__ import YouTube
from pytube import Playlist
from helpers import (
    command_line_parser,
    parse_title,
    song_questionare,
    mp4_to_mp3,
    apply_apic,
    apply_id3,
)


def main(*args):
    ns = command_line_parser(*args)

    def single_song(url):
        yt = YouTube(url)
        stream = (
            yt.streams.filter(only_audio=False, audio_codec="mp4a.40.2")
            .order_by("abr")
            .desc()
        )

        track_info = parse_title(stream[0].title)
        track = track_info["track"]
        artist = track_info["artist"]

        track_info = song_questionare(track_info, ns)
        track = track_info["track"]
        artist = track_info["artist"]

        print("Downloading...")
        stream[0].download(filename=f"{track}.mp4")

        mp4_to_mp3(track)

        apply_apic(track, yt.thumbnail_url)
        apply_id3(track_info)

        os.remove(f"{track}.mp4")

        # windows likes to keep the thumbnail file around after downloading
        for root, dir, files in os.walk("."):
            if "Folder.jpg" in files:
                os.remove("Folder.jpg")
            if "AlbumArtSmall.jpg" in files:
                os.remove("AlbumArtSmall.jpg")

        if args[0]["dir"]:
            os.rename(f"{track}.mp3", f"{args[0]['dir']}\{track}.mp3")

    if ns:
        if ns.playlist:
            playlist = Playlist(ns.link)
            for url in playlist.video_urls:
                single_song(url)
        else:
            single_song(ns.link)
    else:
        single_song(args[0]["link"])


if __name__ == "__main__":
    main()
