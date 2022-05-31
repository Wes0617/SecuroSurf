from __future__ import annotations

from functools import partialmethod

import securosurf_gui_toolkit.toolkit as tk
from securosurf_gui import gui_make_performance_frame
from securosurf_gui import gui_make_game_status_frame
from securosurf_gui import gui_make_notifications_frame
from securosurf_gui import gui_make_configuration_update_frame
from securosurf_gui import gui_make_configuration_selector_frame

########################################################################################################################

def FUNC() -> tk.Container:
    class ColumnText(tk.Text): pass
    ColumnText.__init__ = partialmethod(ColumnText.__init__, size=16)

    return tk.Container([
        [gui_make_configuration_selector_frame.FUNC()],
        [gui_make_game_status_frame.FUNC(ColumnText)],
        [gui_make_configuration_update_frame.FUNC(ColumnText)],
        [gui_make_performance_frame.FUNC(ColumnText)],
        [gui_make_notifications_frame.FUNC(ColumnText)],
        [tk.EmptyRectangle(area=(380, 0))]
    ])
