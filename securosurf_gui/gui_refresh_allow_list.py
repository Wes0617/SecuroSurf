from __future__ import annotations

import securosurf_gui_toolkit.toolkit as tk
from securosurf.session_configuration import SessionConfiguration

########################################################################################################################

def FUNC(
    window: tk.Window,
    SC: SessionConfiguration.CLASS,
    blink: bool,
):
    widget_allow_list_info: tk.Text = window["allow_list_info"]

    show_IP_changed_countdown = SC.allow_list is not None and SC.IP_changed_sync_countdown is not None

    if show_IP_changed_countdown:
        text = "IP changed! Wait {}s before joining an existing lobby!".format(round(SC.IP_changed_sync_countdown))
        appearance = tk.TextAppearance.ERROR if blink else tk.TextAppearance.NORMAL
    else:
        if SC.allow_list is not None:
            only_allows = ["Self"]
            if SC.allow_list.allow_LAN_IPs:
                only_allows.append("Lan")
            if len(SC.allow_list.IPs) > 0:
                only_allows.append(f"{len(SC.allow_list.IPs)} IPs")
            text = "Allows: {}".format(" + ".join(only_allows))
            appearance = tk.TextAppearance.NORMAL
        else:
            text = f"Allows: Anyone"
            appearance = tk.TextAppearance.NORMAL

    widget_allow_list_info.tk_update(text=text, appearance=appearance)
