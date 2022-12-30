from __future__ import annotations

import time
import pydivert
import threading as t
import multiprocessing as m
from pydivert.packet import Packet

from securosurf.firewall import is_LAN_IP
from securosurf.firewall import PacketThrottler
from securosurf.telemetry import PacketInboundT2Throttled

from securosurf.telemetry_manager import TelemetryManager
from securosurf.process_messaging import ProcessMessaging
from securosurf.session_configuration import SessionConfiguration
from securosurf.runtime_configuration import RuntimeConfiguration

from securosurf.telemetry import PacketInboundAllowedStranger
from securosurf.telemetry import PacketInboundStranger
from securosurf.telemetry import PacketInboundAllowList
from securosurf.telemetry import PacketInboundT2
from securosurf.telemetry import PacketInboundT2Heartbeat
from securosurf.telemetry import PacketInboundAllowListLAN
from securosurf.telemetry import PacketOutbound
from securosurf.telemetry import PacketOutboundT2

########################################################################################################################

class CLASS:
    def __init__(
        self,
        messaging: ProcessMessaging.CLASS,
        telemetry_manager: TelemetryManager.CLASS,
        initial_session_configuration: SessionConfiguration.CLASS,
        initial_runtime_configuration: RuntimeConfiguration.CLASS
    ):
        self.__messaging: ProcessMessaging.CLASS                 = messaging
        self.__telemetry_manager: TelemetryManager.CLASS         = telemetry_manager
        self.__process: m.Process                                = m.Process(target=self._run, daemon=True)
        self.__session_configuration: SessionConfiguration.CLASS = initial_session_configuration
        self.__runtime_configuration: RuntimeConfiguration.CLASS = initial_runtime_configuration
        self._T2_servers: set[str]                               = set()

    def start(self):
        pydivert.WinDivert.register()
        self.__process.start()

    def stop(self):
        self.__process.terminate()
        pydivert.WinDivert.unregister()

    def _run(self):
        def _handle_IPC():
            while True:
                returned_message, returned_contents = self.__messaging.receive_message()
                if returned_message == "get_telemetry":
                    self.__messaging.send_message("return_telemetry", self.__telemetry_manager.get_telemetry())
                elif returned_message == "set_session_configuration":
                    self.__session_configuration = returned_contents
                    print("Received session configuration from parent process.")
                elif returned_message == "set_runtime_configuration":
                    self.__runtime_configuration = returned_contents
                    print("Received runtime configuration from parent process.")
        t.Thread(target=_handle_IPC, args=(), daemon=True).start()

        self.T2_throttling = PacketThrottler.CLASS()

        self.SG_throttling = PacketThrottler.CLASS()

        inbound_packet_filter = "(inbound and (" \
                                "    udp.DstPort == 6672" \
                                "    or udp.SrcPort == 6672" \
                                "    or udp.SrcPort == 61455" \
                                "    or udp.SrcPort == 61456" \
                                "    or udp.SrcPort == 61457" \
                                "    or udp.SrcPort == 61458" \
                                "))"

        outbound_packet_filter = "(outbound and (" \
                                "    udp.DstPort == 6672" \
                                "    or udp.SrcPort == 6672" \
                                "    or udp.SrcPort == 61455" \
                                "    or udp.SrcPort == 61456" \
                                "    or udp.SrcPort == 61457" \
                                "    or udp.SrcPort == 61458" \
                                "    or udp.DstPort == 61455" \
                                "    or udp.DstPort == 61456" \
                                "    or udp.DstPort == 61457" \
                                "    or udp.DstPort == 61458" \
                                "))"

        packet_filter = f"udp.PayloadLength > 0 and ip and ({inbound_packet_filter} or {outbound_packet_filter})"

        with pydivert.WinDivert(packet_filter) as win_divert:
            for packet in win_divert:
                if self.__do_allow(packet, time.time()):
                    win_divert.send(packet)

    def __do_allow(self, packet: Packet, now: float):
        ET = True # enable telemetry
        SC = self.__session_configuration
        RC = self.__runtime_configuration
        TM = self.__telemetry_manager
        TM.activity = now

        if packet.is_inbound:
            my_IP = packet.dst_addr
            my_port = packet.dst_port
            rm_IP = packet.src_addr
            rm_port = packet.src_port
        else:
            my_IP = packet.src_addr
            my_port = packet.src_port
            rm_IP = packet.dst_addr
            rm_port = packet.dst_port

        length = len(packet.payload)

        if length in SC.T2_heartbeat_sizes:
            print(f"Found T2 server {rm_IP}")
            self._T2_servers.add(rm_IP)

        if packet.is_inbound:
            if SC.allow_list is not None:
                allow_list_identity = SC.allow_list.IPs.get(rm_IP, None)

                if allow_list_identity is not None:
                    TM.add(PacketInboundAllowList.CLASS(my_IP, my_port, rm_IP, rm_port, length, allow_list_identity)) if ET else None
                    return True

                elif SC.allow_list.allow_LAN_IPs is True and is_LAN_IP.FUNC(rm_IP):
                    TM.add(PacketInboundAllowListLAN.CLASS(my_IP, my_port, rm_IP, rm_port, length)) if ET else None
                    return True

                elif rm_IP in self._T2_servers:
                    if RC.tinfoil_hat_mode is True or (
                        self.T2_throttling is not None and
                        self.T2_throttling.do_throttle(SC.T2_throttling.per_seconds, SC.T2_throttling.max_packets)
                    ):
                        TM.add(PacketInboundT2Throttled.CLASS(my_IP, my_port, rm_IP, rm_port, length)) if ET else None
                        return False

                else:
                    if RC.tinfoil_hat_mode is True or (
                        SC.strangers_throttling is not None and
                        self.SG_throttling.do_throttle(SC.strangers_throttling.per_seconds, SC.strangers_throttling.max_packets)
                    ):
                        TM.add(PacketInboundStranger.CLASS(my_IP, my_port, rm_IP, rm_port, length)) if ET else None
                        return False

            if rm_IP in self._T2_servers:
                if length in SC.T2_heartbeat_sizes:
                    TM.add(PacketInboundT2Heartbeat.CLASS(my_IP, my_port, rm_IP, rm_port, length)) if ET else None
                    return True

                else:
                    TM.host_activity = now
                    TM.add(PacketInboundT2.CLASS(my_IP, my_port, rm_IP, rm_port, length)) if ET else None
                    return True

            TM.add(PacketInboundAllowedStranger.CLASS(my_IP, my_port, rm_IP, rm_port, length)) if ET else None
            return True
        else:
            if rm_IP in self._T2_servers:
                TM.add(PacketOutboundT2.CLASS(my_IP, my_port, rm_IP, rm_port, length)) if ET else None
                return True
            else:
                TM.add(PacketOutbound.CLASS(my_IP, my_port, rm_IP, rm_port, length)) if ET else None
                return True

