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
    widget_update_last_attempted: tk.Text = window["update_last_attempted"]
    widget_update_last_successful: tk.Text = window["update_last_successful"]

    # ------------------------------------------------------------------------------------------------------------------

    if SC_last_update_attempt is None:
        return

    # ------------------------------------------------------------------------------------------------------------------

    SC_last_update_attempt_age = time.time() - SC_last_update_attempt
    SC_age = time.time() - SC.fetch_time
    is_failure = SC_last_update_attempt != SC.fetch_time
    is_paused = not is_failure and SC_age > SC.update_frequency + 10

    # ------------------------------------------------------------------------------------------------------------------

    if is_paused:
        _text = f"Every {SC.update_frequency} seconds (Paused)."
    else:
        _text = f"Every {SC.update_frequency} seconds."

    widget_update_frequency.tk_update(text=_text)

    # ------------------------------------------------------------------------------------------------------------------

    if SC_last_update_attempt_age > (3 * 60):
        _text = f"more than 3 minutes ago."
    else:
        _text = f"{round(SC_last_update_attempt_age)} seconds ago."
    widget_update_last_attempted.tk_update(text=_text)

    # ------------------------------------------------------------------------------------------------------------------

    if SC_age > (3 * 60):
        _text = f"More than 3 minutes ago."
    else:
        _text = f"{round(SC_age)} seconds ago."

    if is_failure:
        _appearance = tk.TextAppearance.ERROR
    elif is_paused:
        _appearance = tk.TextAppearance.NORMAL
    else:
        _appearance = tk.TextAppearance.SUCCESS

    widget_update_last_successful.tk_update(text=_text, appearance=_appearance)
