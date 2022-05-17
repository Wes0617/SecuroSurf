from __future__ import annotations

import time
import securosurf_gui_toolkit.toolkit as tk
from securosurf.session_configuration import SessionConfiguration

########################################################################################################################

def FUNC(
    window: tk.Window,
    session_configuration: SessionConfiguration.CLASS,
    session_configuration_last_update_attempt: float | None
):
    widget_update_frequency: tk.Text = window["update_frequency"]
    widget_update_frequency.tk_update(text=f"Every {session_configuration.update_frequency} seconds.")

    # ------------------------------------------------------------------------------------------------------------------

    if session_configuration_last_update_attempt is None:
        _text = "Never."
    else:
        last_attempt_age = round(time.time() - session_configuration_last_update_attempt)
        _text = "Over an hour ago." if last_attempt_age > 3600 else f"{last_attempt_age} seconds ago."
    widget_update_last_attempted: tk.Text = window["update_last_attempted"]
    widget_update_last_attempted.tk_update(text=_text)

# ------------------------------------------------------------------------------------------------------------------

    session_configuration_age = round(time.time() - session_configuration.fetch_time)
    update_failed = session_configuration_age > session_configuration.update_frequency
    appearance = tk.TextAppearance.ERROR if update_failed else tk.TextAppearance.SUCCESS
    _text = "Over an hour ago." if session_configuration_age > 3600 else f"{session_configuration_age} seconds ago."
    widget_update_last_successful: tk.Text = window["update_last_successful"]
    widget_update_last_successful.tk_update(text=_text, appearance=appearance)
