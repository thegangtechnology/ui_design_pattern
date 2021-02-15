from __future__ import annotations
import threading

from concurrent.futures import ThreadPoolExecutor

import tkinter as ti
from dataclasses import dataclass
import time
from functools import partial, wraps
from tkinter import ttk
from typing import List, Callable


# Suppose we have a data that doesn't fit with standard tkinter varaible
# we still want to notify the ui thread of the change in data as well
# a simple observer callback is not recommended since remember that ui changes
# MUST happen within the ui main thread.

# The way to do this is notify function with in UIState which is empty at first.
# Notify function jobs's is to put event in to que and that's all.
# The binding to actual notify function should be done in the Broker/App/Controller.
# this way we keep the UIState and the View Totally separate.
# In fact i prefer this pattern over magical tkinter variable but the automagic of Variable
# is too nice.

# My suggestion is for simple 1 page program and variable works just variable.
# If it's 2 page + program. Use notify.

def feet2meter(feet: float) -> float:
    time.sleep(2)
    return int(0.3048 * feet * 10000.0 + 0.5) / 10000.0


class CustomEvent:
    DATA_CHANGE = '<<DATA-CHANGE>>'


@dataclass
class UIState:
    feets: ti.StringVar  # magical but not generic communication
    meters: ti.StringVar
    calculating: ti.BooleanVar

    data: List[float]
    notify: Callable[[str], None] = lambda x: None  # note we don't implement it here

    def modify_data(self):
        for i, d in enumerate(self.data):
            self.data[i] = d + 1
        self.notify(CustomEvent.DATA_CHANGE)

    def convert(self):
        self.calculating.set(True)

        def do_it():
            try:
                feet = float(self.feets.get())
                self.meters.set(feet2meter(feet))
                for i in range(5):
                    self.notify(CustomEvent.DATA_CHANGE)
                self.calculating.set(False)
            finally:
                self.calculating.set(False)

        threading.Thread(target=do_it).start()

    @classmethod
    def empty(cls) -> UIState:
        return UIState(
            feets=ti.StringVar(),
            meters=ti.StringVar(),
            calculating=ti.BooleanVar(False),
            data=[1, 2, 3]
        )


class View:
    def __init__(self, root: ti.Tk):
        self.root = root
        root.title("Feet to Meters")
        self.mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe = self.mainframe
        self.feet_entry = ttk.Entry(mainframe, width=7)  # note no variable
        self.meter_label: ttk.Label = ttk.Label(mainframe)
        self.calculate_button = ttk.Button(mainframe, text="Calculate")
        self.feet_unit_label = ttk.Label(mainframe, text="feet")
        self.equivalent_label = ttk.Label(mainframe, text="is equivalent to")
        self.meter_unit_label = ttk.Label(mainframe, text="meters")
        self.layout()

    def layout(self):
        from tkinter import N, W, E, S
        root = self.root
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        mainframe = self.mainframe
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.feet_entry.grid(column=2, row=1, sticky=(W, E))
        self.meter_label.grid(column=2, row=2, sticky=(W, E))
        self.calculate_button.grid(column=3, row=3, sticky=W)
        self.feet_unit_label.grid(column=3, row=1, sticky=W)
        self.equivalent_label.grid(column=1, row=2, sticky=E)
        self.meter_unit_label.grid(column=3, row=2, sticky=W)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)


class App:
    def __init__(self):
        self.root = ti.Tk()
        self.view = View(self.root)
        self.state = UIState.empty()
        self.state.notify = self.root.event_generate
        self.bind(self.view, self.state)

    def bind(self, view: View, state: UIState):
        view.feet_entry.config(textvariable=state.feets)
        view.meter_label.config(textvariable=state.meters)
        view.calculate_button.config(command=state.convert)

        view.root.bind('<Return>', self.on_return_press())

        view.root.bind(CustomEvent.DATA_CHANGE, self.on_data_change)

        state.calculating.trace_add('write', self.on_calculating_change)
        self.on_calculating_change()  # trace_add doesn't do initial sync

    def on_return_press(self, *arg):
        self.state.modify_data()

    def on_calculating_change(self, *arg):
        calculating = self.state.calculating.get()
        if calculating:
            self.view.calculate_button.config(state=ti.DISABLED)
        else:
            self.view.calculate_button.config(state=ti.NORMAL)

    def on_data_change(self, *arg):
        print('here', str(self.state.data))
        self.view.meter_unit_label.config(text=str(self.state.data))

    def run(self):
        self.root.mainloop()


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
