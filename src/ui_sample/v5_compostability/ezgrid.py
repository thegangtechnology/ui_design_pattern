from __future__ import annotations
from dataclasses import dataclass
from tkinter import Widget
import tkinter as ti
from typing import List, Union, Callable, Set


@dataclass
class StickedWidget:
    stickies: Set[str]
    widget: Widget

    @classmethod
    def factory_maker(cls, stickies: List[str]) -> Callable[[Union[StickedWidget, Widget]], StickedWidget]:
        def factory(w: Union[StickedWidget, Widget]) -> StickedWidget:
            if isinstance(w, StickedWidget):
                w.stickies.add(stickies)
                return w
            else:
                return StickedWidget(stickies=set(stickies), widget=w)
        return factory


N = StickedWidget.factory_maker(['N'])
E = StickedWidget.factory_maker(['E'])
W = StickedWidget.factory_maker(['W'])
S = StickedWidget.factory_maker(['S'])
NE = StickedWidget.factory_maker(['N', 'E'])
NW = StickedWidget.factory_maker(['N', 'W'])
NS = StickedWidget.factory_maker(['N', 'S'])
EW = StickedWidget.factory_maker(['E', 'W'])
ES = StickedWidget.factory_maker(['E', 'S'])
WS = StickedWidget.factory_maker(['W', 'S'])
NEW = StickedWidget.factory_maker(['N', 'E', 'W'])
NWS = StickedWidget.factory_maker(['N', 'W', 'S'])
NES = StickedWidget.factory_maker(['N', 'E', 'S'])
EWS = StickedWidget.factory_maker(['E', 'W', 'S'])
NEWS = StickedWidget.factory_maker(['N', 'E', 'W', 'S'])


def place_grid(widgets: List[List[Union[StickedWidget, Widget]]]):
    for i_row, widget_row in enumerate(widgets):
        for i_col, widget in enumerate(widget_row):
            if isinstance(widget, StickedWidget):
                widget.widget.grid(row=i_row, col=i_col, sticky=widget.stickies)
            else:
                widget.grid(row=i_row, col=i_col)
