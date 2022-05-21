from __future__ import annotations

import time
import securosurf_gui_toolkit.toolkit as tk
from securosurf.session_configuration import SessionConfiguration

########################################################################################################################

def FUNC(
    window: tk.Window,
    SC: SessionConfiguration.CLASS,
    SC_last_update_attempt: float | None
):
    widget_update_frequency: tk.Text = window["update_frequency"]
    widget_update_frequency.tk_update(text=f"Every {SC.update_frequency} seconds.")

    # ------------------------------------------------------------------------------------------------------------------

    if SC_last_update_attempt is None:
        _text = "Never."
    else:
        last_attempt_age = round(time.time() - SC_last_update_attempt)
        _text = "More than 5 minutes ago." if last_attempt_age > (5 * 60) else f"{last_attempt_age} seconds ago."
    widget_update_last_attempted: tk.Text = window["update_last_attempted"]
    widget_update_last_attempted.tk_update(text=_text)

    # ------------------------------------------------------------------------------------------------------------------

    _failure_age = 0 if SC_last_update_attempt is None else SC_last_update_attempt - SC.fetch_time
    if _failure_age > 5:
        _appearance = tk.TextAppearance.ERROR
    else:
        SC_age = round(time.time() - SC.fetch_time)
        update_idled = SC_age > SC.update_frequency
        _appearance = tk.TextAppearance.WARNING if update_idled else tk.TextAppearance.SUCCESS

    _SC_age = round(time.time() - SC.fetch_time)
    _text = "More than 5 minutes ago." if _SC_age > (5 * 60) else f"{_SC_age} seconds ago."

    widget_update_last_successful: tk.Text = window["update_last_successful"]
    widget_update_last_successful.tk_update(text=_text, appearance=_appearance)
