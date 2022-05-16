from tkinter import Tk, ttk, N, W, E, S, StringVar
from main import main

root = Tk()
root.title("Autotube")

mainframe = ttk.Frame(root, padding="6 6 6 6")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

link = StringVar()
link_label = ttk.Label(mainframe, text="URL:").grid(column=0, row=1)
link_entry = ttk.Entry(mainframe, width=25, textvariable=link)
link_entry.grid(column=1, row=1, sticky=(W), padx=3)

ttk.Button(
    mainframe, text="Download", command=lambda: main({"link": link.get(), "exe": True})
).grid(column=2, row=1, sticky=(S, E))

root.mainloop()
