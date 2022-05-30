from __future__ import annotations

import securosurf_gui_toolkit.toolkit as tk

########################################################################################################################

def FUNC() -> tk.Frame:
    return tk.Frame(title="T2 Throttling:", layout=[
        [tk.Text(key="T2_throttling_message", justification="center", expand_x=True)],
    ])
