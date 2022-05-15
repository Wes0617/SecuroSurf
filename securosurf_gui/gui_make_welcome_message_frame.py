from __future__ import annotations

import PySimpleGUI as sg
import securosurf_gui_toolkit.toolkit as tk

########################################################################################################################

def FUNC() -> sg.Frame:
    return sg.Frame(
        title="", border_width=tk.border_width, relief=sg.RELIEF_SUNKEN, expand_x=True,
        layout=[[sg.Text(
            "", expand_x=True, key="welcome_message", size=(1, 1), pad=0,
            justification="center", border_width=tk.padding_width * 2,
            text_color=tk.window_FG, relief=sg.RELIEF_FLAT, font=("Segoe UI", 11, "normal")
        )]]
    )

