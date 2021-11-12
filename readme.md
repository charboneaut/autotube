autotube is a simple extension script for pytube designed for mp3 files
it features
* converts pytube's audio .mp4 into .mp3
* appends id3 tags to .mp3 files such as artist and title
* adds the video thumbnail as an APIC id3 tag, which is sorta like the .mp3 thumbnail

# instructions for devs #
1. clone and cd into the root of the repo
2. use poetry or preferred .toml reader to install dependencies
`poetry install` if you're using poetry
3. enable your virtual environment
4. go to ["how to use" section](https://github.com/charboneaut/autotube#how-to-use)

# instructions if you have no idea what you are doing #

## if on windows ##
1. install [git bash](https://gitforwindows.org/) and here's a [guide](https://www.makeuseof.com/install-git-git-bash-windows/)
2. install [python for windows](https://www.python.org/downloads/windows/) another [guide](https://programmingwithjim.wordpress.com/2020/09/08/installing-python-3-in-git-bash-on-windows-10/)
## everyone else ##
3. install [poetry](https://python-poetry.org/docs/), you're looking for the osx / linux / bashonwindows install instructions, prolly something like\
`curl -sSl https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -` but that link might change
4. download the autotube zip file from github and extract its contents
5. navigate to wherever you extracted the files in git bash, by default that would be\
`cd Downloads/autotube-master`
6. install dependencies w/ poetry (may take a while, usually not more than 2-3 minutes)\
`poetry install`
7. enable the virtual environment w/ poetry\
`poetry shell`
8. go to ["how to use" section](https://github.com/charboneaut/autotube#how-to-use)

# how to use #
`python main.py <youtube link>`

## some options ##
using the command above will prompt you with some questions about the link, prolly looks something like\
`Is the song's title "September"? (y/n)`\
if you trust the script to figure these things you can pass a flag to silence them\
`python main.py -s <youtube link>`
### downloading playlists ###\
`python main.py -p <youtube playlist link>`\
the `-p` flag must be passed to download playlists\
privated playlists won't download, make them unlisted or public\

flags can be mixed and matched either like `-sp` or `-s -p`\
i'll prolly add some more options eventually



