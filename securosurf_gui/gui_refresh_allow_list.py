from __future__ import annotations

import PySimpleGUI as sg
import securosurf_gui_toolkit.toolkit as tk
from securosurf.session_configuration import SessionConfiguration

########################################################################################################################

def FUNC(
    window: tk.Window,
    session_configuration: SessionConfiguration.CLASS,
):
    widget_allow_list_info: tk.Text = window["allow_list_info"]

    if session_configuration.allow_list is not None:
        only_allows = ["Self"]
        if session_configuration.allow_list.allow_LAN_IPs:
            only_allows.append("Lan")
        if len(session_configuration.allow_list.IPs) > 0:
            only_allows.append(f"{len(session_configuration.allow_list.IPs)} IPs")
        only_allows_text = " + ".join(only_allows)
        widget_allow_list_info.update(value=f"Allows: {only_allows_text}")
    else:
        widget_allow_list_info.update("Allows: Anyone")
