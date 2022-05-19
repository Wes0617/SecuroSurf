from __future__ import annotations

import PySimpleGUI as sg
import securosurf_gui_toolkit.toolkit as tk

########################################################################################################################

def FUNC(
    new_crew_names: list[str],
    widget_crew_name: tk.Combo,
    widget_to_crew: sg.Radio,
    widget_to_solo: sg.Radio,
) -> None:
    crews_count = len(new_crew_names)
    selected_crew_name = widget_crew_name.get()

    widget_to_crew.update(disabled=crews_count == 0)
    widget_crew_name.update(disabled=crews_count == 0)

    selected_crew_no_longer_exists = crews_count == 0 or selected_crew_name not in new_crew_names

    if selected_crew_no_longer_exists:
        if widget_to_crew.get() is True:
            widget_to_solo.update(value=True)
            print('Switching to "Solo" as the crew "' + selected_crew_name + '" no longer exists.')
        selected_crew_name = new_crew_names[0] if len(new_crew_names) > 0 else None

    widget_crew_name.update(values=new_crew_names, value=selected_crew_name)
