from __future__ import annotations

import pathlib as p
from securosurf import information
from securosurf_gui import gui_make_sidebar
import securosurf_gui_toolkit.toolkit as tk
from securosurf_gui import gui_make_main_toolbar
from securosurf_gui import gui_make_telemetry_frame
from securosurf_gui import gui_make_welcome_message_frame
from securosurf_gui_toolkit.toolkit import TextAppearance

########################################################################################################################

def FUNC(window_title: str, icon_path: p.Path, log_size: int) -> tk.Window:
    layout = [
        [tk.EmptyRectangle(background_color=tk.accent_BG_lighter, area=(3, 3), expand_x=True)],
        [tk.EmptyRectangle(background_color="white", area=(2, 2), expand_x=True)],
        [tk.EmptyRectangle(background_color=tk.accent_BG, area=(8, 8), expand_x=True)],

        [tk.FrameContainer([
            [gui_make_main_toolbar.FUNC()],
            [gui_make_welcome_message_frame.FUNC()],
            [
                gui_make_sidebar.FUNC(),
                gui_make_telemetry_frame.FUNC(log_size)
            ],
        ], expand_x=True, expand_y=True)],

        [tk.EmptyRectangle(background_color=tk.accent_BG, area=(8, 8), expand_x=True)],
        [tk.EmptyRectangle(background_color="white", area=(2, 2), expand_x=True)],
        [tk.EmptyRectangle(background_color=tk.accent_BG_lighter, area=(3, 3), expand_x=True)],

        [tk.FrameContainer([
            [
                tk.Text(
                    text="Tip: If necessary, you can reduce CPU usage by minimizing this window to the taskbar.",
                    appearance=TextAppearance.DISABLED,
                    justification="left", expand_x=True,
                ),
                tk.Text(
                    text=information.VAR.application_full_name,
                    appearance=TextAppearance.DISABLED,
                    justification="right", expand_x=True
                )
            ]
        ], expand_x=True)],
    ]

    return tk.Window(title=window_title, layout=layout, icon=icon_path)
