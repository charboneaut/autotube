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
link_frame.grid(
    column=0,
    row=1,
)
link_label = ttk.Label(link_frame, text="URL:", font=14).grid(column=0, row=0, padx=4)
link_entry = ttk.Entry(link_frame, width=25, textvariable=link, font=14)
link_entry.grid(column=1, row=0, sticky=(W), padx=3)

save_frame = ttk.Frame(mainframe)
save_frame.grid(column=1, row=2)
noti_frame = ttk.Frame(save_frame)
noti_frame.grid(column=0, row=0, sticky=(W), padx=5)


def download_mp4_display():
    main({"link": link.get(), "exe": True, "dir": root.directory})
    with open("track.txt", "r") as file:
        track_info = file.read().split("\n")
        original_title.set(track_info[0])
        track.set(track_info[1])
        artist.set(track_info[2])
        thumb.set(track_info[3])
        pre_desc = track_info[4:]
        desc.set("".join(pre_desc))

    infowars = ttk.Frame(mainframe)
    infowars.grid(column=0, row=2, sticky=(N, W, E, S))
    ttk.Label(infowars, text="Track:", font=14).grid(column=0, row=0)
    ttk.Entry(infowars, textvariable=track, font=14, width=25).grid(
        column=1, row=0, sticky=(W)
    )
    ttk.Label(infowars, text="Artist:", font=14).grid(column=0, row=1)
    ttk.Entry(infowars, textvariable=artist, font=14, width=25).grid(
        column=1, row=1, sticky=(W)
    )
    ttk.Label(infowars, text="Origin:", font=14).grid(column=0, row=2)
    ttk.Label(infowars, text=f"{original_title.get()}", font=14).grid(
        column=1, row=2, sticky=(W)
    )
    ttk.Label(infowars, text=f"{desc.get()}", font=14, wraplength=300).grid(
        column=1, row=3
    )
    ttk.Button(noti_frame, text="Save file...", command=save_file).grid(column=0, row=0)
    preview = Canvas(save_frame, width=640, height=480)
    preview.grid(column=0, row=1, sticky=(N, W, E, S))
    img_data = requests.get(thumb.get()).content
    with open("thumb.jpg", "wb") as file:
        file.write(img_data)
    root.img = img = ImageTk.PhotoImage(file="thumb.jpg")
    preview.create_image(0, 0, anchor=NW, image=img)
    ttk.Label(
        noti_frame,
        text=f"Video downloaded as '{track.get()}.mp4'!",
        foreground="#4bb543",
        font=14,
    ).grid(column=1, row=0, padx=3)


ttk.Button(
    link_frame,
    text="Download",
    command=download_mp4_display,
).grid(column=2, row=0)


def save_file():
    root.directory = filedialog.askdirectory()
    try:
        single_song_exe_save(
            {
                "track": track.get(),
                "artist": artist.get(),
                "url": thumb.get(),
                "dir": root.directory,
            }
        )
    except FileExistsError:
        ttk.Label(
            noti_frame,
            text=f"File already exists in {root.directory}",
            foreground="#fc100d",
            font=14,
        ).grid(column=1, row=0, padx=3)

    ttk.Label(
        noti_frame,
        text=f"Saved as '{track.get()}.mp3!' in {root.directory}",
        foreground="#4bb543",
        font=14,
    ).grid(column=1, row=0, padx=3)


root.mainloop()
