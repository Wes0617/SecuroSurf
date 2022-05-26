from __future__ import annotations

import PySimpleGUI as sg
from functools import partialmethod
import securosurf_gui_toolkit.toolkit as tk

########################################################################################################################

def FUNC(window_telemetry_length: int) -> tk.Frame:
    traffic_table = []

    labels = []
    labels.append("STime:")
    labels.append("Count:")
    labels.append("ETime:")
    labels.append("Local IP:")
    labels.append("\N{white left-pointing triangle}\N{white right-pointing triangle}")
    labels.append("Remote IP:")
    labels.append("Bytes:")
    labels.append("Action:")
    labels.append("Message:")

    keys = []
    keys.append("telemetry_st_")
    keys.append("telemetry_count_")
    keys.append("telemetry_et_")
    keys.append("telemetry_local_IP_")
    keys.append("telemetry_traffic_indicator_")
    keys.append("telemetry_remote_IP_")
    keys.append("telemetry_size_")
    keys.append("telemetry_action_")
    keys.append("telemetry_message_")

    sizes = []
    sizes.append(5 + 2)
    sizes.append(3 + 2)
    sizes.append(5 + 2)
    sizes.append(15 + 2)
    sizes.append(3 + 4)
    sizes.append(15 + 2)
    sizes.append(3 + 2)
    sizes.append(5 + 2)
    sizes.append(25)

    fonts = [("Segoe UI", 8, "normal")] * 9
    fonts[1] = fonts[7] = fonts[8] = ("Segoe UI", 8, "bold")

    traffic_table.append([
        _TitleCell(labels[0], size=sizes[0], font=fonts[0]), _Separator(True),
        _TitleCell(labels[1], size=sizes[1], font=fonts[1]), _Separator(True),
        _TitleCell(labels[2], size=sizes[2], font=fonts[2]), _Separator(True),
        _TitleCell(labels[3], size=sizes[3], font=fonts[3]), _Separator(True),
        _TitleCell(labels[4], size=sizes[4], font=fonts[4]), _Separator(True),
        _TitleCell(labels[5], size=sizes[5], font=fonts[5]), _Separator(True),
        _TitleCell(labels[6], size=sizes[6], font=fonts[6]), _Separator(True),
        _TitleCell(labels[7], size=sizes[7], font=fonts[7]), _Separator(True),
        _TitleCell(labels[8], size=sizes[8], font=fonts[8]),
    ])

    traffic_table.append([_HeadingSeparator()])

    for i in range(0, window_telemetry_length):
        traffic_table.append([
            _Cell(key=f"{keys[0]}{i}", size=sizes[0], font=fonts[0]), _Separator(True),
            _Cell(key=f"{keys[1]}{i}", size=sizes[1], font=fonts[1]), _Separator(True),
            _Cell(key=f"{keys[2]}{i}", size=sizes[2], font=fonts[2]), _Separator(True),
            _Cell(key=f"{keys[3]}{i}", size=sizes[3], font=fonts[3]), _Separator(True),
            _Cell(key=f"{keys[4]}{i}", size=sizes[4], font=fonts[4]), _Separator(True),
            _Cell(key=f"{keys[5]}{i}", size=sizes[5], font=fonts[5],), _Separator(True),
            _Cell(key=f"{keys[6]}{i}", size=sizes[6], font=fonts[6],), _Separator(True),
            _Cell(key=f"{keys[7]}{i}", size=sizes[7], font=fonts[7],), _Separator(True),
            sg.Input(
                key=f"{keys[8]}{i}", size=sizes[8], font=fonts[8],
                pad=(tk.padding_width * 2, 0), border_width=0,
                disabled_readonly_background_color=tk.window_BG,
                readonly=False, disabled=True,
            ),
        ])
        traffic_table.append([_Separator(False)])

    traffic_table.pop()

    return tk.Frame("Telemetry:", layout=[[
        sg.Col(traffic_table, expand_x=True, pad=tk.padding_width),
    ]])

########################################################################################################################

class _Cell(sg.Text): pass
_Cell.__init__ = partialmethod(
    _Cell.__init__, font=("Segoe UI", 8, "normal"),
    justification="center", pad=(tk.padding_width * 2, 0), border_width=0,
)

class _TitleCell(_Cell): pass
_TitleCell.__init__ = partialmethod(
    _TitleCell.__init__, text_color=tk.window_FG_highlight)

class _HeadingSeparator(sg.Col):
    def __init__(self):
        super().__init__(
            layout = [[]], background_color=tk.separator_color,
            pad=(0, tk.padding_width), size=(1, 1), expand_x=True, expand_y=None
        )

class _Separator(sg.Col):
    def __init__(self, vertical: bool):
        expand = {"expand_x": None, "expand_y": True} if vertical else {"expand_x": True, "expand_y": None}
        super().__init__(layout = [[]], background_color=tk.light_separator_color, pad=0, size=(1, 1), **expand)
