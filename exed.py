from tkinter import Tk, ttk, N, W, E, S, StringVar, filedialog
from main import main
from helpers import single_song_exe_save

root = Tk()
root.title("Autotube")
root.directory = ""
original_title = StringVar()
track = StringVar()
artist = StringVar()
thumb = StringVar()

mainframe = ttk.Frame(root, padding="6 6 6 6")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

link = StringVar()
link_label = ttk.Label(mainframe, text="URL:").grid(column=0, row=1)
link_entry = ttk.Entry(mainframe, width=25, textvariable=link)
link_entry.grid(column=1, row=1, sticky=(W), padx=3)


def download_mp4_display():
    main({"link": link.get(), "exe": True, "dir": root.directory})
    with open("track.txt", "r") as file:
        track_info = file.read().split("\n")
        original_title.set(track_info[0])
        track.set(track_info[1])
        artist.set(track_info[2])
        thumb.set(track_info[3])
    ttk.Label(mainframe, text="Track:").grid(column=0, row=2)
    ttk.Label(mainframe, text=f"{track.get()}?").grid(column=1, row=2, sticky=(W))
    ttk.Label(mainframe, text="Artist:").grid(column=0, row=3)
    ttk.Label(mainframe, text=f"{artist.get()}?").grid(column=1, row=3, sticky=(W))
    ttk.Button(mainframe, text="Save file...", command=save_file).grid(
        column=3, row=3, sticky=(S, E)
    )


ttk.Button(
    mainframe,
    text="Download",
    command=download_mp4_display,
).grid(column=3, row=1, sticky=(S, E))


def save_file():
    root.directory = filedialog.askdirectory()
    single_song_exe_save(
        {
            "track": track.get(),
            "artist": artist.get(),
            "url": thumb.get(),
            "dir": root.directory,
        }
    )


root.mainloop()
