from __future__ import annotations

import threading
import time
import tkinter as ti
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import partial
from tkinter import ttk

# Not finished. blame Minmin 5555

def feet2meter(feet: float) -> float:
    time.sleep(2)
    return int(0.3048 * feet * 10000.0 + 0.5) / 10000.0


class Executor: # all aux execution get queue
    _executor = None

    @classmethod
    def get(cls) -> ThreadPoolExecutor:
        if cls._executor is None:
            cls._executor = ThreadPoolExecutor(max_workers=1)
        return cls._executor

@dataclass
class UIState:
    feets: ti.StringVar
    meters: ti.StringVar
    calculating: ti.BooleanVar

    def convert(self):
        self.calculating.set(True)
        feet = float(self.feets.get())

        def do_it():
            self.meters.set(feet2meter(feet))
            self.calculating.set(False)

        threading.Thread(target=do_it).start()

    @classmethod
    def empty(cls) -> UIState:
        return UIState(
            feets=ti.StringVar(),
            meters=ti.StringVar(),
            calculating=ti.BooleanVar(False)
        )


class ConverterView:
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
        self.view = ConverterView(self.root)
        self.state = UIState.empty()
        self.bind(self.view, self.state)

    def bind(self, view: ConverterView, state: UIState):
        view.feet_entry.config(textvariable=state.feets)
        view.meter_label.config(textvariable=state.meters)
        view.calculate_button.config(command=state.convert)
        self.link_button_state_with(view.calculate_button, state.calculating)
        view.root.bind('<Return>', state.convert)

    def link_button_state_with(self, button: ttk.Button, bv: ti.BooleanVar):
        def set_disable(button: ttk.Button, bv: ti.BooleanVar, *arg):
            if bv.get():
                button.config(state=ti.DISABLED)
            else:
                button.config(state=ti.NORMAL)

        bv.trace_add('write', partial(set_disable, button, bv))
        set_disable(button, bv)  # for the initial binding

    def run(self):
        self.root.mainloop()


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
