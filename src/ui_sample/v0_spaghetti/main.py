from __future__ import annotations

import tkinter as ti
from dataclasses import dataclass
import time
from tkinter import ttk
import threading


# straight from tkdoc https://tkdocs.com/tutorial/firstexample.html
# This is what's called spaghetti code. For it's intertwined behavior.

# Copy paste code from internet is the #1 source of spaghetti code.
# Tutorial code typically emphasize brevity(for a good reason).
# But in production code we want maintainability and testability.

# 1) it mixes business logic and presentation. Never do this.
# 2) Business logic is done on the same thread as ui thread. This means business logic is blocking ui.

# This means that new person coming in and want to change some simple behavior will need to know how the whole
# application are tied together. The code is extremely fragile, changing one thing will break another thing.

# The technique shown here is actually framework agnostic. The main idea is the same.
from tkinter import Tk, N, E, W, S, StringVar
from tkinter import ttk


def main():
    root = Tk()
    root.title("Feet to Meters")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    feet = StringVar()
    feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
    feet_entry.grid(column=2, row=1, sticky=(W, E))

    meters = StringVar()

    def calculate(*args):
        try:
            value = float(feet.get())
            from time import sleep
            sleep(10)
            meters.set(int(0.3048 * value * 10000.0 + 0.5) / 10000.0)
        except ValueError:
            pass

    ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

    ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

    ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
    ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
    ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    feet_entry.focus()
    root.bind("<Return>", calculate)

    root.mainloop()


if __name__ == '__main__':
    main()
