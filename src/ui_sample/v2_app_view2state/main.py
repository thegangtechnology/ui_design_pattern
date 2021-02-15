from __future__ import annotations
import threading

import tkinter as ti
from dataclasses import dataclass
import time
from tkinter import ttk


# In this version we create a binder call App which facilitate the communication between UIState and view.
# Couple things to notice in this version
# 1) View has no behavior at all. No text variable. The behavior is define in App.bind.
#      - this means view is totally separate from uistate.
#      - the only object that know both is app.
# 2) The communication is bind via app.bind is only from view to ui state.

#          Text Variable + Next Version
#          ----------------------->
#  UI State         App            View
#          <-----------------------
#           Text Variable + command


def feet2meter(feet: float) -> float:
    time.sleep(2)
    return int(0.3048 * feet * 10000.0 + 0.5) / 10000.0


@dataclass
class UIState:
    feets: ti.StringVar
    meters: ti.StringVar

    def calculate(self):
        feet = float(self.feets.get())

        def do_it():
            self.meters.set(feet2meter(feet))

        threading.Thread(target=do_it).start()

    @classmethod
    def empty(cls) -> UIState:
        return UIState(
            feets=ti.StringVar(),
            meters=ti.StringVar()
        )


class View:
    def __init__(self, root: ti.Tk):
        from tkinter import N, W, E, S
        self.root = root

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.feet_entry = ttk.Entry(mainframe, width=7)  # note no variable
        self.feet_entry.grid(column=2, row=1, sticky=(W, E))

        self.meter_label: ttk.Label = ttk.Label(mainframe)
        self.meter_label.grid(column=2, row=2, sticky=(W, E))

        self.calculate_button = ttk.Button(mainframe, text="Calculate")
        self.calculate_button.grid(column=3, row=3, sticky=W)

        ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)


class App:
    def __init__(self):
        self.root = ti.Tk()
        self.root.title("Feet to Meters")
        self.view = View(self.root)
        self.state = UIState.empty()
        self.bind(self.view, self.state)

    def bind(self, view: View, state: UIState):
        view.feet_entry.config(textvariable=state.feets)
        view.meter_label.config(textvariable=state.meters)
        view.calculate_button.config(command=state.calculate)
        view.root.bind('<Return>', state.calculate)

    def run(self):
        self.root.mainloop()


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
