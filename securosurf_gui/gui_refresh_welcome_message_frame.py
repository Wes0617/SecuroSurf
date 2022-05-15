from __future__ import annotations

import PySimpleGUI as sg
import securosurf_gui_toolkit.toolkit as tk

########################################################################################################################

def FUNC(widget_welcome_message: sg.Text, is_help: bool, text: str):
    if is_help:
        widget_welcome_message.update(text, background_color=tk.window_BG_help, font=("Segoe UI", 11, "normal"))
    else:
        widget_welcome_message.update(text, background_color=tk.window_BG, font=("Segoe UI", 11, "italic"))
