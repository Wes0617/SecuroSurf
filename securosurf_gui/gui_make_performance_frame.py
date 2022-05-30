from __future__ import annotations

import securosurf_gui_toolkit.toolkit as tk
from typing import Type

########################################################################################################################

def FUNC(ColumnTextClass: Type[tk.Text]) -> tk.Frame:
    refresh_rate_slider = tk.Slider(key="refresh_rate", range=(100, 5000), value=100, step=100, expand_x=True, disabled=True)
    refresh_rate_apply = tk.Button(key="set_refresh_rate", text="Apply", appearance=tk.ButtonAppearance.DISABLED)
    telemetry_options = ["Always enabled", "Disabled if minimized", "Always disabled"]
    return tk.Frame("Performance:", layout=[
        [tk.Text("These options are currently not implemented.", justification="center", expand_x=True)],
        [ColumnTextClass("Refresh rate (ms):"), refresh_rate_slider, refresh_rate_apply],
        [ColumnTextClass("Telemetry:"),         tk.Combo(telemetry_options, telemetry_options[0], expand_x=True, disabled=True, readonly=True, key="telemetry_type")],
    ])
