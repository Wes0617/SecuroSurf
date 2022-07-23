from __future__ import annotations

import PySimpleGUI as sg

import sys
import time
import threading as t
import multiprocessing as m

from securosurf.firewall import Firewall
from securosurf.telemetry_manager import TelemetryManager
from securosurf.process_messaging import ProcessMessaging
from securosurf_gui_toolkit.toolkit_tools import EventTarget
from securosurf.session_configuration_manager import SessionConfigurationSetManager
from securosurf.runtime_configuration import RuntimeConfiguration

from securosurf_gui import gui_make
from securosurf_gui import gui_refresh_telemetry
from securosurf_gui import gui_refresh_allow_list
from securosurf_gui import gui_refresh_game_status
from securosurf_gui import gui_refresh_welcome_message
from securosurf_gui import gui_refresh_configuration_update
from securosurf_gui import gui_refresh_configuration_selector

########################################################################################################################

def FUNC(simulation: bool = False) -> None:

    window_refresh_rate_user_ms = 100
    window_refresh_rate_max_ms  = 5000
    window_refresh_rate_used_ms = window_refresh_rate_user_ms
    window_play_bell            = False
    _telemetry_length           = 32
    window                      = gui_make.FUNC(_telemetry_length)
    window_event_target         = EventTarget(window)
    SC_set_manager              = SessionConfigurationSetManager.CLASS()
    SC_name                     = "Normal"
    SC_manager                  = SC_set_manager.get_by_name(SC_name)
    SC                          = SC_manager.get()
    SC_changed                  = False
    RC                          = RuntimeConfiguration.CLASS()
    RC_changed                  = False
    _telemetry_manager          = TelemetryManager.CLASS(_telemetry_length)
    firewall_telemetry          = _telemetry_manager.get_telemetry()
    _messaging                  = ProcessMessaging.CLASS(m.Queue(), m.Queue())
    firewall                    = Firewall.CLASS(_messaging.invert(), _telemetry_manager, SC, RC)
    firewall.start()

    # ------------------------------------------------------------------------------------------------------------------

    def _handle_IPC_thread():
        nonlocal firewall_telemetry, SC_changed, RC_changed
        while True:
            _messaging.send_message("get_telemetry")
            returned_message, returned_contents = _messaging.receive_message()

            if returned_message == "return_telemetry":
                firewall_telemetry = returned_contents

            if SC_changed:
                SC_changed = False
                _messaging.send_message("set_session_configuration", SC)

            if RC_changed:
                RC_changed = False
                _messaging.send_message("set_runtime_configuration", RC)

            time.sleep(window_refresh_rate_used_ms / 1000)
    t.Thread(target=_handle_IPC_thread, args=(), daemon=True).start()

    # ------------------------------------------------------------------------------------------------------------------

    def _fetch_configuration_thread():
        nonlocal SC_manager, SC, SC_changed, window_play_bell
        while True:
            last_fetched_SC_name = SC_name
            SC_manager = SC_set_manager.get_by_name(last_fetched_SC_name)

            _new_SC = SC_manager.get()
            if _new_SC != SC:
                SC_changed = True
                if _new_SC.allow_list is not None and _new_SC.allow_list.IP_changed:
                    window_play_bell = True
            SC = _new_SC

            fetch_SC_again_time = time.time() + SC.update_frequency
            while True:
                time.sleep(1)
                if SC_name != last_fetched_SC_name:
                    break
                if firewall_telemetry.is_active is False:
                    continue
                if time.time() >= fetch_SC_again_time:
                    break
    t.Thread(target=_fetch_configuration_thread, args=(), daemon=True).start()

    # ------------------------------------------------------------------------------------------------------------------

    widget_message: sg.Text = window["welcome_message"]

    from securosurf_gui.application_help import VAR as _help_messages
    window_showing_help = False

    def _show_help_message(_element_key: str):
        nonlocal window_showing_help
        gui_refresh_welcome_message.FUNC(widget_message, True, _help_messages.get(_element_key, ""))
        window_showing_help = True

    def show_welcome_message():
        nonlocal window_showing_help
        gui_refresh_welcome_message.FUNC(widget_message, False, SC.welcome_message)
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

        _window_blink_last = locals().get("_window_blink_last", time.time())
        window_blink = locals().get("window_blink", True)
        if time.time() > _window_blink_last + 0.5:
            window_blink = not window_blink
            _window_blink_last = time.time()

        # --------------------------------------------------------------------------------------------------------------

        # Tkinter changes the mouse pointer to load and leaves it like that forever. This seems to fix it.
        window.TKroot.config(cursor='')

        # --------------------------------------------------------------------------------------------------------------

        _is_minimized = window.tk_get_metrics().state == "iconic"
        window_refresh_rate_used_ms = window_refresh_rate_max_ms if _is_minimized else window_refresh_rate_user_ms

        _new_metrics = window.tk_get_metrics()
        if _new_metrics != locals().get("_last_known_metrics", None):
            _last_known_metrics = _new_metrics
            print(_new_metrics)

        # --------------------------------------------------------------------------------------------------------------

        _new_crew_names = SC_set_manager.get_crew_names()
        _user_selected_a_crew_in_combo_box = event_name == "crew_name"
        SC_name = gui_refresh_configuration_selector.FUNC(window, _new_crew_names, _user_selected_a_crew_in_combo_box)

        # --------------------------------------------------------------------------------------------------------------

        _new_RC = RuntimeConfiguration.CLASS(window["job_mode"].get())
        if _new_RC != RC:
            RC = _new_RC
            RC_changed = True

        # --------------------------------------------------------------------------------------------------------------

        if not window_showing_help:
            show_welcome_message()

        # --------------------------------------------------------------------------------------------------------------

        if window_play_bell:
            window.ding()
            window_play_bell = False

        # --------------------------------------------------------------------------------------------------------------

        gui_refresh_allow_list          .FUNC(window, SC, window_blink)
        gui_refresh_game_status         .FUNC(window, firewall_telemetry)
        gui_refresh_configuration_update.FUNC(window, SC, SC_manager.last_update_attempt)
        gui_refresh_telemetry           .FUNC(window, firewall_telemetry)

        window.refresh()

    firewall.stop()
    window.close()
