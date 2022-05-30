from __future__ import annotations

import securosurf_gui_toolkit.toolkit as tk
from typing import Type

########################################################################################################################

def FUNC(ColumnTextClass: Type[tk.Text]) -> tk.Frame:
    notifications_options = ["Disable", "Enable"]
    return tk.Frame(title="Notifications:", layout=[
        [ColumnTextClass("On join:"),      tk.Combo(notifications_options, notifications_options[0], expand_x=True, disabled=True, readonly=True, key="enable_join_notifications")],
        [ColumnTextClass("On leave:"),     tk.Combo(notifications_options, notifications_options[0], expand_x=True, disabled=True, readonly=True, key="enable_leave_notifications")],
        [ColumnTextClass("On IP Change:"), tk.Combo(notifications_options, notifications_options[1], expand_x=True, disabled=True, readonly=True, key="enable_IP_change_notifications")],
    ])
