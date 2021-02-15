from __future__ import annotations

import tkinter as ti
from dataclasses import dataclass
import time
from tkinter import ttk
from typing import TypeVar, Generic, Callable
import threading


def feet2meter(feet: float) -> float:
    time.sleep(2)
    return int(0.3048 * feet * 10000.0 + 0.5) / 10000.0


@dataclass
class UIState:
    feet: ti.StringVar
    meters: ti.StringVar

    def calculate(self):
        def make_job():
            feet = float(self.feet.get())
            def ret():
                self.meters.set(feet2meter(feet))
            return ret
        job = make_job()
        threading.Thread(target=job).start()


    @classmethod
    def empty(cls) -> UIState:
        return UIState(
            feet=ti.StringVar(),
            meters=ti.StringVar()
        )


def build_ui(root: ti.Tk, state: UIState) -> ti.Tk:
    from tkinter import N, W, E, S

    root.title("Feet to Meters")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    feet_entry = ttk.Entry(mainframe, width=7, textvariable=state.feet)
    feet_entry.grid(column=2, row=1, sticky=(W, E))

    ttk.Label(mainframe, textvariable=state.meters).grid(column=2, row=2, sticky=(W, E))

    ttk.Button(mainframe, text="Calculate", command=state.calculate).grid(column=3, row=3, sticky=W)

    ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
    ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
    ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    feet_entry.focus()
    root.bind("<Return>", state.calculate)

    return root


def main():
    root = ti.Tk()
    state = UIState.empty()
    ui = build_ui(root, state)
    ui.mainloop()
