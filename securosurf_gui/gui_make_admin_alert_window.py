from __future__ import annotations

import pathlib as p
from securosurf import information
import securosurf_gui_toolkit.toolkit as tk
from securosurf_gui_toolkit.toolkit import TextAppearance

########################################################################################################################

def FUNC(window_title: str, icon_path: p.Path, message: str) -> tk.Window:
    layout = [
        [tk.EmptyRectangle(background_color=tk.accent_BG_lighter, area=(3, 3), expand_x=True)],
        [tk.EmptyRectangle(background_color="white", area=(2, 2), expand_x=True)],
        [tk.EmptyRectangle(background_color=tk.accent_BG, area=(8, 8), expand_x=True)],

        [tk.FrameContainer([[
            tk.Frame(title="Error!", title_icon=tk.Icon.WARNING, layout=[[
                tk.AlertPadding([
                    [tk.Text(message)],
                ])
            ]])
        ]])],

        [tk.EmptyRectangle(background_color=tk.accent_BG, area=(8, 8), expand_x=True)],
        [tk.EmptyRectangle(background_color="white", area=(2, 2), expand_x=True)],
        [tk.EmptyRectangle(background_color=tk.accent_BG_lighter, area=(3, 3), expand_x=True)],

        [tk.FrameContainer([[tk.Text(
            text=information.VAR.application_full_name,
            appearance=TextAppearance.DISABLED,
            justification="right", expand_x=True,
        )]], expand_x=True)],
    ]

    return tk.Window(title=window_title, layout=layout, icon=icon_path)
