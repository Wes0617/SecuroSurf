from __future__ import annotations

import securosurf_gui_toolkit.toolkit as tk
from securosurf.session_configuration import SessionConfiguration

########################################################################################################################

def FUNC(
    window: tk.Window,
    session_configuration: SessionConfiguration.CLASS,
):
    widget_T2_packet_throttling_frame: tk.Frame = window["T2_packet_throttling_frame"]
    widget_T2_packet_throttling_message: tk.Text = window["T2_packet_throttling_message"]

    enabled = session_configuration.T2_packet_throttling is not None

    title_icon = tk.Icon.BALLOT_CHECK if enabled else tk.Icon.BALLOT_EMPTY
    widget_T2_packet_throttling_frame.tk_update(title_icon=title_icon)

    if enabled:
        max_packets = session_configuration.T2_packet_throttling.max_packets
        per_seconds = session_configuration.T2_packet_throttling.per_seconds
        message = f"Limit to {max_packets} packets every {per_seconds} seconds."
    else:
        message = "This functionality is disabled."

    widget_T2_packet_throttling_message.update(value=message)
