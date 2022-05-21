from __future__ import annotations

import pathlib as p
import PySimpleGUI as sg
from securosurf import information
import securosurf_gui_toolkit.toolkit as tk
from securosurf_gui_toolkit.toolkit import TextAppearance

########################################################################################################################

def FUNC() -> None:
    message = f"Unable to start! Please use \"Run as Administrator\" to launch {information.VAR.application_name}!"

    layout = [
        [tk.EmptyRectangle(background_color=tk.accent_BG_lighter, area=(3, 3), expand_x=True)],
        [tk.EmptyRectangle(background_color="white", area=(2, 2), expand_x=True)],
        [tk.EmptyRectangle(background_color=tk.accent_BG, area=(8, 8), expand_x=True)],

        [tk.FrameContainer([[
            tk.Frame(title="Error!", title_icon=tk.Icon.WARNING, layout=[[
                tk.AlertPadding([
                    [tk.Text(message)],
                ])
            ]])
        ]])],

        [tk.EmptyRectangle(background_color=tk.accent_BG, area=(8, 8), expand_x=True)],
        [tk.EmptyRectangle(background_color="white", area=(2, 2), expand_x=True)],
        [tk.EmptyRectangle(background_color=tk.accent_BG_lighter, area=(3, 3), expand_x=True)],

        [tk.FrameContainer([[tk.Text(
            text=information.VAR.application_full_name,
            appearance=TextAppearance.DISABLED,
            justification="right", expand_x=True,
        )]], expand_x=True)],
    ]

    window = tk.Window(title=information.VAR.application_name, layout=layout, icon=information.VAR.icon_path)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: break
    window.close()


