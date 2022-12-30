from __future__ import annotations

import time
import datetime as dt
import collections as c
import PySimpleGUI as sg
import securosurf_gui_toolkit.toolkit as tk
from securosurf_gui import tools_obfuscate_IP
from securosurf.telemetry_manager import Telemetry
from securosurf.telemetry_manager import LiveTraffic
from securosurf.telemetry import PacketOutbound
from securosurf.telemetry import PacketOutboundT2
from securosurf.telemetry import PacketInboundT2
from securosurf.telemetry import PacketInboundStranger
from securosurf.telemetry import PacketInboundAllowList
from securosurf.telemetry import PacketInboundT2Throttled
from securosurf.telemetry import PacketInboundT2Heartbeat
from securosurf.telemetry import PacketInboundAllowListLAN
from securosurf.telemetry import PacketInboundAllowedStranger

########################################################################################################################

def _time(time: float) -> str:
    return dt.datetime.utcfromtimestamp(time).strftime("%M:%S")

def FUNC(window: tk.Window, firewall_telemetry: Telemetry.CLASS):

    traffic: c.deque[LiveTraffic.CLASS] = firewall_telemetry.traffic

    old_packet_age = 30
    log_size = traffic.maxlen
    assert(log_size is not None)

    i = -1
    for live_traffic in traffic:
        i += 1

        widget_st: sg.Text = window[f"telemetry_st_{i}"]
        widget_et: sg.Text = window[f"telemetry_et_{i}"]
        widget_local_IP: sg.Text = window[f"telemetry_local_IP_{i}"]
        widget_traffic_indicator: sg.Text = window[f"telemetry_traffic_indicator_{i}"]
        widget_remote_IP: sg.Text = window[f"telemetry_remote_IP_{i}"]
        widget_size: sg.Text = window[f"telemetry_size_{i}"]
        widget_count: sg.Text = window[f"telemetry_count_{i}"]
        widget_packets_per_s: sg.Text = window[f"telemetry_packets_per_s_{i}"]
        widget_action: sg.Text = window[f"telemetry_action_{i}"]
        widget_message: sg.Input = window[f"telemetry_message_{i}"]

        start_packet = live_traffic.start_packet
        end_packet = live_traffic.end_packet

        if end_packet.inbound:
            traffic_indicator_on = "\N{black left-pointing triangle}"
            traffic_indicator_off = "\N{white left-pointing triangle}"
            traffic_indicator_color = "red"
        else:
            traffic_indicator_on = "\N{black right-pointing triangle}"
            traffic_indicator_off = "\N{white right-pointing triangle}"
            traffic_indicator_color = "green"

        end_packet_age = time.time() - live_traffic.end_packet.time

        if end_packet_age < old_packet_age:
            _step = live_traffic.count % 3
            traffic_indicator_text = [traffic_indicator_on] * 3
            traffic_indicator_text[_step] = traffic_indicator_off
            FG = tk.window_FG
            FG_success = tk.window_FG_success
            FG_warning = tk.window_FG_warning
            FG_error = tk.window_FG_error
            FG_highlight = tk.window_FG_highlight
            FG_disabled = tk.window_FG_disabled
        else:
            traffic_indicator_text = [traffic_indicator_off] * 3
            FG = tk.window_FG_faded
            FG_success = tk.window_FG_success_faded
            FG_warning = tk.window_FG_warning_faded
            FG_error = tk.window_FG_error_faded
            FG_highlight = tk.window_FG_highlight_faded
            FG_disabled = tk.window_FG_disabled_faded

        widget_st.update(_time(start_packet.time), text_color=FG)

        widget_et.update(_time(end_packet.time), text_color=FG)

        widget_local_IP.update(end_packet.local_IP + f":{end_packet.local_port}", text_color=FG)

        widget_traffic_indicator.update("".join(traffic_indicator_text), text_color=traffic_indicator_color)

        formatted_remote_IP = tools_obfuscate_IP.FUNC(end_packet.remote_IP) + f":{end_packet.remote_port}"
        widget_remote_IP.update(formatted_remote_IP, text_color=FG)

        widget_size.update(f"{end_packet.size}", text_color=FG)

        widget_count.update(str(live_traffic.count), text_color=FG)

        elapsed_time = end_packet.time - start_packet.time
        if elapsed_time == 0:
            packets_per_s = "-"
        else:
            packets_per_s = round(live_traffic.count / elapsed_time, 2)
            packets_per_s = str(packets_per_s)

        widget_packets_per_s.update(packets_per_s, text_color=FG)

        allow = lambda: widget_action.update("ALLOW", text_color=FG_success)
        block = lambda: widget_action.update("BLOCK", text_color=FG_error)

        if isinstance(end_packet, PacketInboundT2Heartbeat.CLASS):
            widget_message.update("T2 Heartbeat", text_color=FG_warning)
            allow()
        elif isinstance(end_packet, PacketInboundT2.CLASS):
            widget_message.update("T2 Packets", text_color=FG_warning)
            allow()
        elif isinstance(end_packet, PacketInboundT2Throttled.CLASS):
            widget_message.update("T2 Throttled Packet", text_color=FG_error)
            block()

        elif isinstance(end_packet, PacketInboundAllowList.CLASS):
            end_packet: PacketInboundAllowList.CLASS
            widget_message.update(end_packet.identity, text_color=FG_highlight)
            allow()
        elif isinstance(end_packet, PacketInboundAllowListLAN.CLASS):
            widget_message.update("Lan Computer", text_color=FG_highlight)
            allow()
        elif isinstance(end_packet, PacketInboundAllowedStranger.CLASS):
            widget_message.update("Stranger", text_color=FG_disabled)
            allow()
        elif isinstance(end_packet, PacketInboundStranger.CLASS):
            widget_message.update("Stranger", text_color=FG_error)
            block()
        elif isinstance(end_packet, PacketOutboundT2.CLASS):
            widget_message.update("Outbound T2", text_color=FG_warning)
            allow()
        elif isinstance(end_packet, PacketOutbound.CLASS):
            widget_message.update("Outbound", text_color=FG_disabled)
            allow()
        else:
            raise "unknown type"
