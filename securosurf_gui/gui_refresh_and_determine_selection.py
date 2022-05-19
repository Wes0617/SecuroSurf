from __future__ import annotations

import PySimpleGUI as sg
from securosurf_gui import gui_refresh_crew_names
import securosurf_gui_toolkit.toolkit as tk

########################################################################################################################

CurrentSessionConfigurationName = str

def FUNC(
    window: tk.Window,
    new_crew_names: list[str],
    triggered_by_crew_name_change: bool
) -> CurrentSessionConfigurationName:

    widget_to_normal: sg.Radio = window["to_normal"]
    widget_to_solo: sg.Radio = window["to_solo"]
    widget_to_LAN: sg.Radio = window["to_LAN"]
    widget_to_dyn: sg.Radio = window["to_dynamic"]
    widget_to_crew: sg.Radio = window["to_crew"]
    widget_crew_name: sg.Combo = window["crew_name"]
    widget_crew_name.Widget.selection_range(0, 0)

    gui_refresh_crew_names.FUNC(new_crew_names, widget_crew_name, widget_to_crew, widget_to_solo)

    if triggered_by_crew_name_change:
        widget_to_crew.update(value=True)

    if widget_to_normal.get():
        session_configuration_name = "Normal"
    elif widget_to_solo.get():
        session_configuration_name = "Solo"
    elif widget_to_LAN.get():
        session_configuration_name = "LAN"
    elif widget_to_dyn.get():
        session_configuration_name = "Dynamic"
    elif widget_to_crew.get():
        session_configuration_name = widget_crew_name.get()
    else:
        raise Exception()

    return session_configuration_name
