from __future__ import annotations

import PySimpleGUI as sg
import securosurf_gui_toolkit.toolkit as tk
from securosurf.session_configuration_manager import SessionConfigurationManager

########################################################################################################################

def FUNC(
    session_configuration_manager: SessionConfigurationManager.CLASS,
    current_crew_names: list[str],
    widget_crew_name: tk.Combo,
    widget_to_crew: sg.Radio,
    widget_to_solo: sg.Radio,
) -> list[str]:
    crew_names = session_configuration_manager.get_crew_names()
    if crew_names == current_crew_names:
        return current_crew_names

    crews_count = len(crew_names)
    selected_crew_name = widget_crew_name.get()

    widget_to_crew.update(disabled=crews_count == 0)
    widget_crew_name.update(disabled=crews_count == 0)

    selected_crew_no_longer_exists = crews_count == 0 or selected_crew_name not in crew_names

    if selected_crew_no_longer_exists:
        if widget_to_crew.get() is True:
            widget_to_solo.update(value=True)
            print('Switching to "Solo" as the crew "' + selected_crew_name + '" no longer exists.')
        selected_crew_name = crew_names[0] if len(crew_names) > 0 else None

    widget_crew_name.update(values=crew_names, value=selected_crew_name)

    return crew_names
