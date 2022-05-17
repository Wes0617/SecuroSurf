from __future__ import annotations

import securosurf_gui_toolkit.toolkit as tk
from securosurf.telemetry_manager import Telemetry

########################################################################################################################

def FUNC(
    window: tk.Window,
    telemetry: Telemetry.CLASS,
    active_max_age_minutes: int,
    host_max_age_minutes: int,
):
    widget_traffic_last_activity: tk.Text = window["traffic_last_activity"]

    if telemetry.last_activity is None or telemetry.last_activity_age > (active_max_age_minutes * 60):
        text = "The game appears closed."
        appearance = tk.TextAppearance.WARNING
    elif telemetry.last_activity_age <= 1:
        text = "Just now."
        appearance = tk.TextAppearance.SUCCESS
    else:
        text = f"{round(telemetry.last_activity_age)} seconds ago."
        appearance = tk.TextAppearance.NORMAL

    widget_traffic_last_activity.tk_update(text=text, appearance=appearance)

    # ------------------------------------------------------------------------------------------------------------------

    widget_traffic_host_last_activity: tk.Text = window["traffic_host_last_activity"]

    if telemetry.last_T2_host_packet is None or telemetry.last_T2_host_packet_age > (host_max_age_minutes * 60):
        text = f"You appear not to be hosting."
        appearance = tk.TextAppearance.NORMAL
    else:
        text = f"{round(telemetry.last_T2_host_packet_age)} seconds ago (Hosting)."
        appearance = tk.TextAppearance.SUCCESS

    widget_traffic_host_last_activity.tk_update(text=text, appearance=appearance)
