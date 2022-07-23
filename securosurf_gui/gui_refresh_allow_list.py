from __future__ import annotations

import securosurf_gui_toolkit.toolkit as tk
from securosurf.session_configuration import SessionConfiguration

########################################################################################################################

def FUNC(
    window: tk.Window,
    SC: SessionConfiguration.CLASS,
    blink: bool,
):
    widget_filter_info: tk.Text = window["filter_info"]

    # ------------------------------------------------------------------------------------------------------------------

    show_IP_changed_countdown = SC.allow_list is not None and SC.IP_changed_sync_countdown is not None
    if show_IP_changed_countdown:
        text = "IP changed! Wait {}s before joining an existing lobby!".format(round(SC.IP_changed_sync_countdown))
        appearance = tk.TextAppearance.ERROR if blink else tk.TextAppearance.NORMAL
        widget_filter_info.update(text)
        return

    # ------------------------------------------------------------------------------------------------------------------

    filter_spec = []

    if SC.allow_list is None:
        filter_spec.append("Anyone")
    else:
        filter_spec.append("Self")

        if SC.allow_list.allow_LAN_IPs:
            filter_spec.append("Lan")

        if len(SC.allow_list.IPs) > 0:
            filter_spec.append(f"{len(SC.allow_list.IPs)} IPs")

        if SC.T2_throttling is not None:
            max_packets = SC.T2_throttling.max_packets
            per_seconds = SC.T2_throttling.per_seconds
            filter_spec.append(f"{max_packets}T2s/{per_seconds}s")

        if SC.strangers_throttling is not None:
            max_packets = SC.strangers_throttling.max_packets
            per_seconds = SC.strangers_throttling.per_seconds
            filter_spec.append(f"{max_packets}SGs/{per_seconds}s")

    _text = "Allows: " + (" + ".join(filter_spec))
    widget_filter_info.update(_text)
