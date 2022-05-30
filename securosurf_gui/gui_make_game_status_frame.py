from __future__ import annotations

import securosurf_gui_toolkit.toolkit as tk
from typing import Type

########################################################################################################################

def FUNC(ColumnTextClass: Type[tk.Text]) -> tk.Frame:
    return tk.Frame(title="Game Status:", layout=[
        [ColumnTextClass("Last activity:"),      tk.Text(key="traffic_last_activity", expand_x=True)],
        [ColumnTextClass("Last host activity:"), tk.Text(key="traffic_host_last_activity", expand_x=True)],
    ])
