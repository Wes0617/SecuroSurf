from __future__ import annotations

import time
import securosurf_gui_toolkit.toolkit as tk
from securosurf.session_configuration import SessionConfiguration
from securosurf.session_configuration_manager import LiveSessionConfiguration

########################################################################################################################

def FUNC(
    window: tk.Window,
    live_session_configuration: LiveSessionConfiguration.CLASS,
):
    session_configuration = live_session_configuration.get()

    widget_update_frequency: tk.Text = window["update_frequency"]
    widget_update_last_attempted: tk.Text = window["update_last_attempted"]
    widget_update_last_successful: tk.Text = window["update_last_successful"]

    widget_update_frequency.tk_update(text=f"{session_configuration.update_frequency} seconds")

    if live_session_configuration.latest_update_attempt is None:
        last_attempt_age_text = "Never"
    else:
        last_attempt_age = round(time.time() - live_session_configuration.latest_update_attempt)
        last_attempt_age_text = "Over an hour ago" if last_attempt_age > 3600 else f"{last_attempt_age} seconds ago"
    widget_update_last_attempted.tk_update(text=last_attempt_age_text)

    session_configuration_age = round(time.time() - session_configuration.fetch_time)
    update_failed = session_configuration_age > session_configuration.update_frequency
    appearance = tk.TextAppearance.ERROR if update_failed else tk.TextAppearance.SUCCESS
    sc_age_text = "Over an hour ago" if session_configuration_age > 3600 else f"{session_configuration_age} seconds ago"

    widget_update_last_successful.tk_update(text=sc_age_text, appearance=appearance)
