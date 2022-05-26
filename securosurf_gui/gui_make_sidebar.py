from __future__ import annotations

import PySimpleGUI as sg
from functools import partialmethod
import securosurf_gui_toolkit.toolkit as tk

########################################################################################################################

def FUNC() -> tk.Container:
    class ColumnText(tk.Text): pass
    ColumnText.__init__ = partialmethod(ColumnText.__init__, size=16)
    column_width = 371

    f1 = tk.Frame("Allow-list:", layout=[
        [tk.Text(key="allow_list_info", expand_x=True, justification="center")],
    ])

    f2 = tk.Frame(title="T2 Throttling:", layout=[
        [tk.Text(key="T2_throttling_message", justification="center", expand_x=True)],
    ])

    f3 = tk.Frame(title="Traffic Status:", layout=[
        [ColumnText("Last activity:"),          tk.Text(key="traffic_last_activity", expand_x=True)],
        [ColumnText("Last host activity:"),     tk.Text(key="traffic_host_last_activity", expand_x=True)],
    ])

    f4 = tk.Frame(title="Configuration Update:", layout=[
        [ColumnText("Frequency:"),              tk.Text(key="update_frequency", expand_x=True)],
        [ColumnText("Last attempted:"),         tk.Text(key="update_last_attempted", expand_x=True)],
        [ColumnText("Last successful:"),        tk.Text(key="update_last_successful", expand_x=True)],
    ])

    refresh_rate_slider = tk.Slider(key="refresh_rate", range=(100, 5000), value=100, step=100, expand_x=True, disabled=True)
    refresh_rate_apply = tk.Button(key="set_refresh_rate", text="Apply", appearance=tk.ButtonAppearance.DISABLED)
    telemetry_options = ["Always enabled", "Disabled if minimized", "Always disabled"]
    f5 = tk.Frame("Performance:", layout=[
        [tk.Text("These options are currently not implemented.", justification="center", expand_x=True)],
        [ColumnText("Refresh rate (ms):"),      refresh_rate_slider, refresh_rate_apply],
        [ColumnText("Telemetry:"),              tk.Combo(telemetry_options, telemetry_options[0], expand_x=True, disabled=True, readonly=True, key="telemetry_type")],
    ])

    notifications_options = ["Disable", "Enable"]
    f6 = tk.Frame(title="Notifications:", layout=[
        [tk.Text("These options are currently not implemented.", justification="center", expand_x=True)],
        [ColumnText("On join:"),                tk.Combo(notifications_options, notifications_options[0], expand_x=True, disabled=True, readonly=True, key="enable_join_notifications")],
        [ColumnText("On leave:"),               tk.Combo(notifications_options, notifications_options[0], expand_x=True, disabled=True, readonly=True, key="enable_leave_notifications")],
    ])

    return tk.Container([
        [f1], [f2], [f3], [f4], [f5], [f6], [tk.EmptyRectangle(area=(column_width, 0))]
    ])
