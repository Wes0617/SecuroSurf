from __future__ import annotations

import pathlib as p
import PySimpleGUI as sg
from securosurf import information
from securosurf_gui import gui_make_admin_alert_window

########################################################################################################################

def FUNC(root: p.Path) -> None:
    message = f"Unable to start! Please use \"Run as Administrator\" to launch {information.VAR.application_name}!"

    _icon_path = root / "images" / "icon.ico"
    window = gui_make_admin_alert_window.FUNC(information.VAR.application_name, _icon_path, message)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: break
    window.close()
