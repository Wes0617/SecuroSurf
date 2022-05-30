from __future__ import annotations

import securosurf_gui_toolkit.toolkit as tk

########################################################################################################################

def FUNC() -> tk.Frame:
    return tk.Frame("Allow-list:", layout=[
        [tk.Text(key="allow_list_info", expand_x=True, justification="center")],
    ])
