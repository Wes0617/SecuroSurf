from __future__ import annotations

import securosurf_gui_toolkit.toolkit as tk
from typing import Type

########################################################################################################################

def FUNC(ColumnTextClass: Type[tk.Text]) -> tk.Frame:
    return tk.Frame(title="Configuration Update:", layout=[
        [ColumnTextClass("Frequency:"),       tk.Text(key="update_frequency", expand_x=True)],
        [ColumnTextClass("Last attempted:"),  tk.Text(key="update_last_attempted", expand_x=True)],
        [ColumnTextClass("Last successful:"), tk.Text(key="update_last_successful", expand_x=True)],
    ])
