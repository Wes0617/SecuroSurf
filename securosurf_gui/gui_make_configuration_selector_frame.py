from __future__ import annotations

import PySimpleGUI as sg
from functools import partialmethod
import securosurf_gui_toolkit.toolkit as tk

########################################################################################################################

def FUNC() -> tk.Frame:
    labels = ["Normal", "Solo", "Lan", "Crew"]
    keys = ["to_normal", "to_solo", "to_LAN", "to_crew"]

    class Radio(sg.Radio): pass
    Radio.__init__ = partialmethod(Radio.__init__, enable_events=True, pad=(tk.padding_width, 0))
    group = "session_type_change"

    tinfoil_hat_mode = sg.Checkbox("Tinfoil Hat", False, key="tinfoil_hat_mode", enable_events=True, disabled=True)

    return tk.Frame(layout=[
        [
            Radio(labels[0], group, key=keys[0], default=True),
            Radio(labels[1], group, key=keys[1]),
            Radio(labels[2], group, key=keys[2]),
            Radio(labels[3], group, key=keys[3], disabled=True),
            tinfoil_hat_mode,
        ],
        [tk.Combo([], disabled=True, enable_events=True, readonly=True, key="crew_name", expand_x=True)],
        [sg.Input(key="filter_info", expand_x=True, justification="center")],
    ])
