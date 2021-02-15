from __future__ import annotations

import threading
import time
import tkinter as ti
from dataclasses import dataclass
from tkinter import ttk

# We have the  missing communication piece which is state change -> change in view
# this can be done via trace.

# Trace on the surface may look like just
# class ObservableInt:
#    data : int
#    callbacks: List[Callable]
#    def set_data(self, data):
#        self.data = data
#        for cb in self.callbacks:
#            cb()
#
# But it is way more complicated in threaded environment.
# remember that ui changes must happen in the main thread only. Most UI system works this way.
# If the observable int is change with in a worker thread. Then the callback is called with in the worker thread.
# That means the callback for changing ui will get executed in the worker thread.

# To way trace works is by the event que. Whenever the data is change the event is pushed to event que
# then in the main loop(of ui thread) it keeps dequeing and perform appropriate action.
# Note how the meters.set is done with in the loop

# In the next section we will learn how to do this ourselves for a more complicated data type that
# doesn't fit variable anymore.

def feet2meter(feet: float) -> float:
    time.sleep(2)
    return int(0.3048 * feet * 10000.0 + 0.5) / 10000.0


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
        self.bind(self.view, self.state)

    def bind(self, view: View, state: UIState):
        view.feet_entry.config(textvariable=state.feets)
        view.meter_label.config(textvariable=state.meters)
        view.calculate_button.config(command=state.convert)
        view.root.bind('<Return>', state.convert)

        state.calculating.trace_add('write', self.on_calculating_change)
        self.on_calculating_change()  # trace_add doesn't do initial sync

    def on_calculating_change(self, *arg):
        calculating = self.state.calculating.get()
        if calculating:
            self.view.calculate_button.config(state=ti.DISABLED)
        else:
            self.view.calculate_button.config(state=ti.NORMAL)

    def run(self):
        self.root.mainloop()


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
