from __future__ import annotations

import PySimpleGUI as sg

import sys
import time
import pathlib as p
import threading as t
import multiprocessing as m

from securosurf.firewall import Firewall
from securosurf.firewall import FirewallFake
from securosurf.telemetry_manager import TelemetryManager
from securosurf.process_messaging import ProcessMessaging
from securosurf.session_configuration_manager import SessionConfigurationManager

from securosurf_gui import gui_make_window
from securosurf_gui import gui_refresh_and_get_session_configuration_names
from securosurf_gui import gui_refresh_telemetry_frame
from securosurf_gui import gui_refresh_update_frame
from securosurf_gui import gui_refresh_allow_list_frame
from securosurf_gui import gui_refresh_status_frame
from securosurf_gui import gui_refresh_welcome_message_frame
from securosurf_gui import gui_refresh_T2_packet_throttling_frame
from securosurf_gui_toolkit.toolkit_tools import EventTarget
from securosurf import information

########################################################################################################################

def FUNC(root: p.Path, simulation: bool = False) -> None:

    active_max_age_minutes              = 3
    host_max_age_minutes                = 4
    window_refresh_rate_user_ms         = 100
    window_refresh_rate_max_ms          = 5000
    window_refresh_rate_used_ms         = window_refresh_rate_user_ms
    _telemetry_length                   = 40
    window                              = gui_make_window.FUNC(root, _telemetry_length)
    window_event_target                 = EventTarget(window)
    session_configuration_manager       = SessionConfigurationManager.CLASS(root)
    current_crew_names                  = []
    session_configuration_name          = "Normal"
    live_session_configuration          = session_configuration_manager.get_by_name(session_configuration_name)
    session_configuration               = live_session_configuration.get()
    session_configuration_changed       = False
    _telemetry_manager                  = TelemetryManager.CLASS(_telemetry_length)
    firewall_telemetry                  = _telemetry_manager.get_telemetry()
    _messaging                          = ProcessMessaging.CLASS(m.Queue(), m.Queue())
    FirewallClass                       = FirewallFake if simulation else Firewall
    firewall                            = FirewallClass.CLASS(_messaging.invert(), _telemetry_manager, session_configuration)
    firewall.start()

    # ------------------------------------------------------------------------------------------------------------------

    def _handle_IPC():
        nonlocal firewall_telemetry
        nonlocal session_configuration_changed
        while True:
            _messaging.send_message("get_telemetry")
            returned_message, returned_contents = _messaging.receive_message()
            if returned_message == "return_telemetry":
                firewall_telemetry = returned_contents
            if session_configuration_changed:
                session_configuration_changed = False
                _messaging.send_message("set_session_configuration", session_configuration)
            time.sleep(window_refresh_rate_used_ms / 1000)
    t.Thread(target=_handle_IPC, args=(), daemon=True).start()

    # ------------------------------------------------------------------------------------------------------------------

    widget_message: sg.Text = window["welcome_message"]

    from securosurf_gui.application_help import VAR as _help_messages
    window_showing_help = False

    def _show_help_message(_element_key: str):
        nonlocal window_showing_help
        gui_refresh_welcome_message_frame.FUNC(widget_message, True, _help_messages.get(_element_key, ""))
        window_showing_help = True

    def show_welcome_message():
        nonlocal window_showing_help
        gui_refresh_welcome_message_frame.FUNC(widget_message, False, session_configuration.welcome_message)
        window_showing_help = False

    for _element_key in _help_messages:
        window_event_target.add_event_listener(_element_key, "<Enter>", lambda elk, evk: _show_help_message(elk))
        window_event_target.add_event_listener(_element_key, "<Leave>", lambda elk, evk: show_welcome_message())

    # ------------------------------------------------------------------------------------------------------------------

    while True:
        event_name, _values = window.read(window_refresh_rate_used_ms)
        if event_name != "__TIMEOUT__": print("Event: " + str(event_name), file=sys.stderr)
        if event_name == sg.WIN_CLOSED: break
        window_event_target.run_event_listeners(event_name)

        # --------------------------------------------------------------------------------------------------------------

        window.TKroot.config(cursor='')

        # --------------------------------------------------------------------------------------------------------------

        _is_minimized = window.tk_get_metrics().state == "iconic"
        window_refresh_rate_used_ms = window_refresh_rate_max_ms if _is_minimized else window_refresh_rate_user_ms

        _new_metrics = window.tk_get_metrics()
        if _new_metrics != locals().get("_last_known_metrics", None):
            _last_known_metrics = _new_metrics
            print(_new_metrics)

        # --------------------------------------------------------------------------------------------------------------

        current_crew_names, session_configuration_name = gui_refresh_and_get_session_configuration_names.FUNC(
            window, session_configuration_manager, current_crew_names, event_name == "crew_name"
        )

        live_session_configuration = session_configuration_manager.get_by_name(session_configuration_name)
        _new_session_configuration = live_session_configuration.get()
        if _new_session_configuration != session_configuration:
            session_configuration_changed = True
            session_configuration = _new_session_configuration

        if not window_showing_help:
            show_welcome_message()

        gui_refresh_allow_list_frame          .FUNC(window, session_configuration)
        gui_refresh_status_frame              .FUNC(window, firewall_telemetry, active_max_age_minutes, host_max_age_minutes)
        gui_refresh_T2_packet_throttling_frame.FUNC(window, session_configuration)
        gui_refresh_update_frame              .FUNC(window, live_session_configuration)
        gui_refresh_telemetry_frame           .FUNC(window, firewall_telemetry)

        window.refresh()

    firewall.stop()
    window.close()
