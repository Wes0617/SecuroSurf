from __future__ import annotations

from enum import Enum
from pathlib import Path
import PySimpleGUI as sg
from dataclasses import dataclass
from functools import partialmethod

########################################################################################################################

def is_darkmode():
    # Author: https://stackoverflow.com/a/65349866/4251625
    try:
        import winreg
    except ImportError:
        return False
    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
    reg_keypath = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
    try:
        reg_key = winreg.OpenKey(registry, reg_keypath)
    except FileNotFoundError:
        return False

    for i in range(1024):
        try:
            value_name, value, _ = winreg.EnumValue(reg_key, i)
            if value_name == 'AppsUseLightTheme':
                return value == 0
        except OSError:
            break
    return False

########################################################################################################################

def FG_brightness(color):
    return color.hex

print("Is dark-mode:", is_darkmode())

padding_width                       = 3
border_width                        = 1 # combos' border is always 1, so this should be always be 1 for consistency

accent_BG                           = "#0C529A"
accent_BG_lighter                   = "#1A7ED4"
accent_FG                           = "white"

separator_color                     = "#A1A1A1"
light_separator_color               = "#E2E2E2"

window_font                         = ("Segoe UI", 9, "normal")
window_BG                           = "white"
window_BG_help                      = "#FBFCC5"
window_BG_text                      = window_BG # Useful for debugging. Otherwise, should be set to window_BG
window_FG                           = "black"
window_FG_error                     = "red"
window_FG_warning                   = "#DC9B00"
window_FG_highlight                 = "#0C529A"
window_FG_success                   = "green"
window_FG_disabled                  = "#8C8C8C"
window_FG_faded                     = "#BBBBBB"
window_FG_error_faded               = "#FABBBB"
window_FG_warning_faded             = "#F1E1BB"
window_FG_highlight_faded           = "#BDCFE1"
window_FG_success_faded             = "#BBDABB"
window_FG_disabled_faded            = "#DDDDDD"

frame_font                          = ("Segoe UI", 9, "bold")
frame_FG                            = accent_BG # Background is window_BG

button_font                         = ("Verdana", 8, "normal")
button_FG                           = "white"
button_BG                           = accent_BG
button_BG_error                     = "red"
button_BG_warning                   = "orange"
button_BG_success                   = "green"
button_BG_pressed                   = "black"
button_BG_disabled                  = window_BG # disabled buttons always have light gray text, so the bg must not be dark

slider_BG                           = "white"
slider_font                         = ("Verdana", 5, "normal")
slider_min_width                    = 25

combo_background_color              = "white"
combo_text_color                    = "black"
combo_button_background_color       = accent_BG
combo_button_arrow_color            = "white"
combo_font                          = ("Arial", 11, "normal")

########################################################################################################################

assert padding_width >= border_width
padding_exclusive_of_border_width = padding_width - border_width

########################################################################################################################

_theme = {
    # Text Inputs
    "BORDER": border_width, "INPUT": "white", "TEXT_INPUT": "black",

    # Slider
    "SCROLL": accent_BG, "SLIDER_DEPTH": border_width,

    "PROGRESS": ('red', 'blue'),
    "PROGRESS_DEPTH": 0,
}

########################################################################################################################

@dataclass(frozen=True)
class Rect:
    x: int
    y: int

########################################################################################################################
# Icons
########################################################################################################################

class Icon(Enum):
    CROSS_MARK          = "\N{CROSS MARK}"
    BALLOT_CHECK        = "\N{BALLOT BOX WITH CHECK}"
    BALLOT_EMPTY        = "\N{WHITE LARGE SQUARE}"
    HEART               = "\N{WHITE HEART}"
    EYE                 = "\N{EYE}"
    CAR                 = "\N{AUTOMOBILE}"
    BELL                = "\N{BELL}"
    STATS               = "\N{CHART WITH UPWARDS TREND}"
    PERSON              = "\N{BUST IN SILHOUETTE}"
    COCKTAIL            = "\N{COCKTAIL GLASS}"
    RUNNER              = "\N{RUNNER}"
    WARNING             = "\N{WARNING SIGN}"
    STATUS              = "\N{BLACK QUESTION MARK ORNAMENT}"

########################################################################################################################
# Window
########################################################################################################################

@dataclass(frozen=True)
class WindowMetrics:
    screen: Rect
    coords: Rect
    window: Rect
    state: str

class Window(sg.Window):
    def __init__(
        self,
        # Contents
        title: str = "",
        layout: list[list[sg.Element]] | None = None,
        # Events
        # Appearance
        icon: Path | None = None,
        minimizable: bool = True,
        position: tuple[int | None, int | None] = (None, None)
    ):
        super().__init__(
            # Contents
            title=title,
            layout=layout,
            # Events
            # Appearance
            location=position,
            icon=None if icon is None else str(icon),
            # Extra
            finalize=True,
            margins=(0, 0),
            font=window_font,
           # alpha_channel=0.925,
            element_padding=padding_width,
            grab_anywhere_using_control=False,

            # size
            # modal
            # scaling
            # resizable
            # keep_on_top
            # disable_close
            # force_toplevel
            # debugger_enabled
            # disable_minimize
            # transparent_color
            # relative_location

            # auto_size_text
            # auto_size_buttons
            # text_justification
            # default_element_size
            # element_justification
            # default_button_element_size

            # progress_bar_color
            # background_color
            # border_depth
            # button_color

            # auto_close
            # auto_close_duration
            # enable_close_attempted_event
            # return_keyboard_events
            # use_default_focus

            # ttk_theme
            # use_ttk_buttons

            # right_click_menu
            # right_click_menu_background_color
            # right_click_menu_text_color
            # right_click_menu_disabled_text_color
            # right_click_menu_selected_colors
            # right_click_menu_font
            # right_click_menu_tearoff

            # no_titlebar
            # use_custom_titlebar
            # titlebar_background_color
            # titlebar_text_color
            # titlebar_font
            # titlebar_icon

            # grab_anywhere
            # grab_anywhere_using_control

            # metadata
        )

    def tk_get_metrics(self) -> WindowMetrics:
        x, y = sg.Window.get_screen_size()
        screen = Rect(x, y)

        x, y = self.current_location(True)
        coords = Rect(x, y)

        x, y = (self.TKroot.winfo_width(), self.TKroot.winfo_height())
        window = Rect(x, y)

        state = self.TKroot.state()

        return WindowMetrics(screen, coords, window, state)


_theme["BACKGROUND"] = window_BG
_theme["TEXT"] = window_FG

########################################################################################################################
# AlertPadding
########################################################################################################################

class AlertPadding(sg.Column):
    def __init__(
        self,
        layout: list[list[sg.Element]] | None = None,
    ):
        super().__init__(layout, pad=padding_width * 10)


########################################################################################################################
# FrameContainer
########################################################################################################################

class FrameContainer(sg.Column): pass
FrameContainer.__init__ = partialmethod(
    FrameContainer.__init__, vertical_alignment="top", pad=padding_width
)

########################################################################################################################
# Frame
########################################################################################################################

class Frame(sg.Frame):
    def __init__(
        self,
        # Contents
        title: str = "",
        title_icon: Icon | None = None,
        layout: list[list[sg.Element]] | None = None,
        # Events
        key: str | None = None,
        # Appearance
        expand_x: bool = True,
        expand_y: bool = False,
        area: tuple[int | None, int | None] = (None, None),
    ):
        self.__title = title
        self.__title_icon = title_icon

        super().__init__(
            # Contents
            layout=[[sg.Column(layout, expand_y=True, expand_x=True, pad=padding_width)]],
            title=self.__get_full_title(),
            # Events
            key=key,
            # Appearance
            size=area,
            expand_x=expand_x,
            expand_y=expand_y,
            title_location="nw", # this is not an error
            # Extra
            font=frame_font,
            title_color=frame_FG,
            relief=sg.RELIEF_GROOVE,
            border_width=border_width,

            # pad
            # grab
            # tooltip
            # visible
            # metadata
            # right_click_menu
            # background_color
            # vertical_alignment
            # element_justification
        )

    def __get_full_title(self) -> str:
        title_components = []
        if self.__title_icon is not None:
            title_components.append(self.__title_icon.value)
        if self.__title != "":
            title_components.append(self.__title)
        return " ".join(title_components)

    def tk_update(
        self,
        title: str | None = None,
        title_icon: Icon | None = None,
    ):
        self.__title = self.__title if title is None else title
        self.__title_icon = self.__title_icon if title_icon is None else title_icon
        self.update(value=self.__get_full_title())

########################################################################################################################
# Container
########################################################################################################################

class Container(sg.Column): pass
Container.__init__ = partialmethod(
    Container.__init__, vertical_alignment="top", pad=0
)

########################################################################################################################
# VerticalSeparator
########################################################################################################################

class VerticalSeparator(sg.Column):
    def __init__(self):
        super().__init__(
            [[]], background_color=separator_color, size=(1, window_font[1] * 2), pad=padding_width
        )

########################################################################################################################
# Text
########################################################################################################################

class TextAppearance(Enum):
    NORMAL = 1
    ERROR = 2
    WARNING = 3
    SUCCESS = 4
    DISABLED = 5

class Text(sg.Text):
    def __init__(
        self,
        # Contents
        text: str = "",
        # Events
        key: str | None = None,
        enable_events: bool = False,
        # Appearance
        expand_x: bool = False,
        expand_y: bool = False,
        justification: str = "left",
        appearance: TextAppearance = TextAppearance.NORMAL,
        size: tuple[int | None, int | None] = (None, None),
    ):
        self.__appearance = appearance
        super().__init__(
            # Contents
            text=text,
            # Events
            key=key,
            enable_events=enable_events,
            # Appearance
            size=size,
            expand_x=expand_x,
            expand_y=expand_y,
            justification=justification,
            # Extra
            text_color=self.__get_FG(),
            background_color=window_BG,

            # grab
            # tooltip
            # metadata
            # right_click_menu
            # click_submits DEPRECATED

            # pad
            # font
            # relief
            # visible
            # border_width
            # auto_size_text
        )

    def __get_FG(self) -> str:
        if self.__appearance is TextAppearance.SUCCESS:
            return window_FG_success
        elif self.__appearance is TextAppearance.WARNING:
            return window_FG_warning
        elif self.__appearance is TextAppearance.ERROR:
            return window_FG_error
        elif self.__appearance is TextAppearance.DISABLED:
            return window_FG_disabled
        else:
            return window_FG

    def tk_update(
        self,
        text: str | None = None,
        appearance: TextAppearance | None = None,
    ):
        self.__appearance = appearance if appearance is not None else self.__appearance
        self.update(value=text, text_color=self.__get_FG())

########################################################################################################################
# Button
########################################################################################################################

class ButtonAppearance(Enum):
    NORMAL = 1
    ERROR = 2
    WARNING = 3
    SUCCESS = 4
    DISABLED = 5

class Button(sg.Button):
    def __init__(
        self,
        # Contents
        text: str = "",
        # Events
        key: str | None = None,
        # Appearance
        expand_x: bool = False,
        expand_y: bool = False,
        size: tuple[int | None, int | None] = (None, None),
        appearance: ButtonAppearance = ButtonAppearance.NORMAL,
    ):
        self.__appearance = appearance
        disabled = self.__appearance is ButtonAppearance.DISABLED

        super().__init__(
            # Contents
            button_text=text,
            # Events
            key=key,
            # Appearance
            size=size,
            expand_x=expand_x,
            expand_y=expand_y,
            # Extra
            font=button_font,
            disabled=disabled,
            button_color=self.__get_BG(),
            mouseover_colors=button_BG_pressed,
            auto_size_button=True, # TODO check how this affects size=
            # disabled_button_color=button_disabled_background_color, TODO doesn't appear to be working

            # button_type | You should NOT be setting this directly. ONLY the shortcut functions set this
            # change_submits | DEPRECATED
            # highlight_colors | Only works on linux.

            # use_ttk_buttons

            # tooltip
            # metadata

            # focus
            # target
            # visible
            # enable_events
            # bind_return_key
            # right_click_menu

            # file_types
            # initial_folder
            # default_extension

            # image_data
            # image_size
            # image_source
            # image_filename
            # image_subsample
        )

    def __get_BG(self) -> str:
        if self.__appearance is ButtonAppearance.SUCCESS:
            return button_BG_success
        elif self.__appearance is ButtonAppearance.WARNING:
            return button_BG_warning
        elif self.__appearance is ButtonAppearance.ERROR:
            return button_BG_error
        elif self.__appearance is ButtonAppearance.DISABLED:
            return button_BG_disabled
        else:
            return button_BG

    def tk_update(
        self,
        text: str | None = None,
        appearance: ButtonAppearance | None = None,
    ):
        self.__appearance = appearance if appearance is not None else self.__appearance
        disabled = self.__appearance is ButtonAppearance.DISABLED
        self.update(
            text=text,
            disabled=disabled,
            button_color=self.__get_BG()
        )

_theme["BUTTON"] = (button_FG, button_BG)

########################################################################################################################
# Slider
########################################################################################################################

class Slider(sg.Slider):
    def __init__(
        self,
        # Contents
        range: tuple[int|float, int|float] = (0, 100),
        value: int | float = 50,
        step: int | float = 1,
        # Events
        key: str | None = None,
        # Appearance
        expand_x: bool = False,
        disabled: bool = False,
    ):
        super().__init__(
            # Contents
            range=range,
            default_value=value,
            resolution=step,
            # Events
            key=key,
            # Appearance
            expand_x=expand_x,
            disabled=disabled,

            # tick_interval - Prints the value every tick_interval values. Looks awful.
            # disable_number_display
            # change_submits
            # enable_events
            # text_color
            # tooltip
            # visible
            # metadata

            expand_y=None, # Not an error. False causes the element to stretch vertically
            orientation="h",
            font=slider_font,
            relief=sg.RELIEF_FLAT,
            trough_color=slider_BG,
            border_width=border_width,
            background_color=window_BG,
            size=(25, padding_width * 2),
            pad=(padding_exclusive_of_border_width, 0),
        )

    def tk_update(self, value=None, range=(None, None), disabled=None, visible=None):
        pass

########################################################################################################################
# Combo
########################################################################################################################

class Combo(sg.Combo):
    def __init__(
        self, values, default_value=None, size=(None, None), bind_return_key=False,
        enable_events=False, disabled=False, key=None, expand_x=False, expand_y=False,
        tooltip=None, readonly=False, visible=True, metadata=None
    ):
        super().__init__(

            values, default_value=default_value, size=size, bind_return_key=bind_return_key,
            enable_events=enable_events, disabled=disabled, key=key, expand_x=expand_x, expand_y=expand_y,
            tooltip=tooltip, readonly=readonly, visible=visible, metadata=metadata,


            font=combo_font,
            pad=padding_width,
            text_color=combo_text_color, background_color=combo_background_color,
            button_background_color=combo_button_background_color, button_arrow_color=combo_button_arrow_color,
            auto_size_text=True,
        )

########################################################################################################################
# EmptyRectangle
########################################################################################################################

class EmptyRectangle(sg.Column):
    def __init__(
        self,
        layout: list[list[sg.Element]] = None,
        background_color: str = None,
        area: tuple[int | None, int | None] = (None, None),
        pad: tuple[int | None, int | None] = (None, None),
        expand_x: bool | None = None,
        expand_y: bool | None = None,
        vertical_alignment: str = "center"
    ):
        super().__init__(
            layout=[] if layout is None else layout,
            background_color=background_color,
            size=area,
            pad=pad,
            vertical_alignment=vertical_alignment,
            expand_x=expand_x,
            expand_y=expand_y,
        )

########################################################################################################################

sg.theme_add_new('SecuroSurf', _theme)
sg.theme('SecuroSurf')
