from __future__ import annotations

import tkinter as ti
from dataclasses import dataclass
import time
from functools import wraps
from tkinter import ttk
import threading


# In this version we
# 1) separate ui_state from view.
# 2) calculation is done in another thread so it's not blocking
# This separation is extremely important since now UIState is unit-testable no need to click and such.
# Yes the code is longer but we always prefer testability/maintainability over brevity.

# This is decent for small program
# I lied. There is actually a third component to ui which we hid under the rug. The signal.

#    Change in state, reflect in view
#            --------->
#  UI State              View
#            <---------
# Action in View trigger change in UIState

# tkinter provides some basic functionality for 2 ways binding such as textvariable and stringvar.
# this is how it's currently done magically behind the scene.

# But something more advance isn't provide straight away
# for example, if we want to disable right after we click
# this can be done via button.config(state=ti.DISABLED)
# but this breaks the separation between UIState and View

# This is why we need the third component Binder/Presenter/Controller depending on how you want to name it
# to facilitate the communications

def feet2meter(feet: float) -> float:
    # time.sleep(2)
    return int(0.3048 * feet * 10000.0 + 0.5) / 10000.0


@dataclass
class UIState:
    feet: ti.StringVar
    meters: ti.StringVar

    def calculate(self):
        feet = float(self.feet.get())

        def do_it():
            self.meters.set(feet2meter(feet))
            print('done', flush=True)

        t = threading.Thread(target=do_it)  # you could also use concurrent.future for easier debugging
        t.start()

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


def tk_test(f):
    @wraps(f)
    def ret(*arg, **kwds):
        root = ti.Tk()
        root.withdraw()
        def do_f_wait_quit():
            try:
                for timeout in f(*arg, **kwds):
                    threshold = time.time() + timeout
                    while time.time() < threshold:
                        root.update()
                        time.sleep(0.1)
            finally:
                root.destroy()
        root.after('idle', do_f_wait_quit)
        root.mainloop()
    return ret



@tk_test
def test_ui_state_calculate():
    # no clicking
    print('hello')
    state = UIState.empty()
    state.feet.set('100')
    state.calculate()
    yield 1.  # same as wait
    # now check
    assert abs(float(state.meters.get()) - 30.48) < 1e-2
    yield 1
    assert abs(float(state.meters.get()) - 30.48) > 1e-2


if __name__ == '__main__':
    # main()
    test_ui_state_calculate()
