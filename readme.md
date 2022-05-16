autotube is a simple extension script for pytube designed for mp3 files
it features

- converts pytube's audio .mp4 into .mp3
- appends id3 tags to .mp3 files such as artist and title
- adds the video thumbnail as an APIC id3 tag, which is sorta like the .mp3 thumbnail

# instructions for devs

1. clone and cd into the root of the repo
2. use poetry or preferred .toml reader to install dependencies
   `poetry install` if you're using poetry
3. enable your virtual environment
4. go to ["how to use" section](https://github.com/charboneaut/autotube#how-to-use)

# instructions if you have no idea what you are doing

use the new .exe version instead much easier

# how to use command line utility

`python main.py <youtube link>`

## some options

using the command above will prompt you with some questions about the link, prolly looks something like\
`Is the song's title "September"? (y/n)`\
if you trust the script to figure these things you can pass a flag to silence them\
`python main.py -s <youtube link>`

### downloading playlists

`python main.py -p <youtube playlist link>`\
the `-p` flag must be passed to download playlists\
privated playlists won't download, make them unlisted or public

flags can be mixed and matched either like `-sp` or `-s -p`\
i'll prolly add some more options eventually
