from tkinter import NW, Tk, ttk, N, W, E, S, StringVar, filedialog, Canvas
from main import main
from helpers import single_song_exe_save
from PIL import ImageTk
import requests


root = Tk()
root.title("Autotube")
root.directory = ""
original_title = StringVar()
track = StringVar()
artist = StringVar()
thumb = StringVar()
desc = StringVar()

mainframe = ttk.Frame(root, padding="6 6 6 6")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

link = StringVar()
link_frame = ttk.Frame(mainframe)
link_frame.grid(column=0, row=1)
link_label = ttk.Label(link_frame, text="URL:").grid(column=0, row=0)
link_entry = ttk.Entry(link_frame, width=25, textvariable=link)
link_entry.grid(column=1, row=0, sticky=(W), padx=3)


def download_mp4_display():
    main({"link": link.get(), "exe": True, "dir": root.directory})
    with open("track.txt", "r") as file:
        track_info = file.read().split("\n")
        original_title.set(track_info[0])
        track.set(track_info[1])
        artist.set(track_info[2])
        thumb.set(track_info[3])
        desc.set(track_info[4:])

    infowars = ttk.Frame(mainframe)
    infowars.grid(column=0, row=2, sticky=(N, W, E, S))
    ttk.Label(infowars, text="Track:").grid(column=0, row=0)
    ttk.Entry(infowars, textvariable=track).grid(column=1, row=0, sticky=(W))
    ttk.Label(infowars, text="Artist:").grid(column=0, row=1)
    ttk.Entry(infowars, textvariable=artist).grid(column=1, row=1, sticky=(W))
    ttk.Label(infowars, text="Origin:").grid(column=0, row=2)
    ttk.Label(infowars, text=f"{original_title.get()}").grid(
        column=1, row=2, sticky=(W)
    )
    ttk.Label(infowars, text=f"{desc.get()}", wraplength=300).grid(column=1, row=3)
    ttk.Button(mainframe, text="Save file...", command=save_file).grid(
        column=3, row=3, sticky=(S, E)
    )
    preview = Canvas(mainframe, width=480, height=360)
    preview.grid(column=2, row=2, padx=5, pady=2, sticky=(N, W, E, S))
    img_data = requests.get(thumb.get()).content
    with open("thumb.jpg", "wb") as file:
        file.write(img_data)
    root.img = img = ImageTk.PhotoImage(file="thumb.jpg")
    preview.create_image(0, 0, anchor=NW, image=img)


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
