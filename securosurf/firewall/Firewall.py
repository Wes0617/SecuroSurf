from __future__ import annotations

import time
import pydivert
import threading as t
import collections as c
import multiprocessing as m
from pydivert.packet import Packet

from securosurf.firewall import is_LAN_IP
from securosurf.firewall import PacketThrottler
from securosurf.telemetry import PacketInboundT2Throttled

from securosurf.telemetry_manager import TelemetryManager
from securosurf.process_messaging import ProcessMessaging
from securosurf.session_configuration import SessionConfiguration

from securosurf.telemetry import PacketInboundStrangersPhoneInvites
from securosurf.telemetry import PacketInboundAllowedStranger
from securosurf.telemetry import PacketInboundStranger
from securosurf.telemetry import PacketInboundAllowList
from securosurf.telemetry import PacketInboundT2
from securosurf.telemetry import PacketInboundT2Heartbeat
from securosurf.telemetry import PacketInboundAllowListLAN

########################################################################################################################

class CLASS:
    def __init__(
        self,
        messaging: ProcessMessaging.CLASS,
        telemetry_manager: TelemetryManager.CLASS,
        initial_session_configuration: SessionConfiguration.CLASS,
    ):
        self.__messaging: ProcessMessaging.CLASS                 = messaging
        self.__telemetry_manager: TelemetryManager.CLASS         = telemetry_manager
        self.__process: m.Process                                = m.Process(target=self._run, daemon=True)
        self.__session_configuration: SessionConfiguration.CLASS = initial_session_configuration
        self.__matchmaking_servers: set[str]                     = set()

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
        t.Thread(target=_handle_IPC, args=(), daemon=True).start()

        self.T2_throttling = PacketThrottler.CLASS()
        self.SG_throttling = PacketThrottler.CLASS()

        packet_filter = "inbound and udp.DstPort == 6672 and udp.PayloadLength > 0 and ip"
        with pydivert.WinDivert(packet_filter) as win_divert:
            for packet in win_divert:
                if self.__do_allow(packet):
                    win_divert.send(packet)

    def __do_allow(self, packet: Packet):
        ET = True # enable telemetry

        SC = self.__session_configuration

        SB = True # soft block
        SB_per_seconds = 120
        SB_max_packets = 60

        TM = self.__telemetry_manager
        TM.activity = time.time()

        my_ip = packet.dst_addr if packet.is_inbound else packet.src_addr
        rm_ip = packet.dst_addr if packet.is_outbound else packet.src_addr
        length = len(packet.payload)

        if length in SC.T2_heartbeat_sizes:
            self.__matchmaking_servers.add(rm_ip)
            TM.add(PacketInboundT2Heartbeat.CLASS(my_ip, rm_ip, length)) if ET else None
            return True

        if rm_ip in self.__matchmaking_servers:
            TM.host_activity = time.time()

            if SC.T2_throttling is not None:
                if self.T2_throttling.do_throttle(SC.T2_throttling.per_seconds, SC.T2_throttling.max_packets):
                    TM.add(PacketInboundT2Throttled.CLASS(my_ip, rm_ip, length)) if ET else None
                    return False

            TM.add(PacketInboundT2.CLASS(my_ip, rm_ip, length)) if ET else None
            return True

        if SC.allow_list is None:
            TM.add(PacketInboundAllowedStranger.CLASS(my_ip, rm_ip, length)) if ET else None
            return True

        if SC.allow_list.allow_LAN_IPs is True and is_LAN_IP.FUNC(rm_ip):
            TM.add(PacketInboundAllowListLAN.CLASS(my_ip, rm_ip, length)) if ET else None
            return True

        allow_list_message = SC.allow_list.IPs.get(rm_ip, None)
        if allow_list_message is not None:
            TM.add(PacketInboundAllowList.CLASS(my_ip, rm_ip, length, allow_list_message)) if ET else None
            return True

        if SB:
            if self.SG_throttling.do_throttle(SB_per_seconds, SB_max_packets):
                TM.add(PacketInboundStranger.CLASS(my_ip, rm_ip, length)) if ET else None
                return False

            TM.add(PacketInboundStrangersPhoneInvites.CLASS(my_ip, rm_ip, length)) if ET else None
            return True

        TM.add(PacketInboundStranger.CLASS(my_ip, rm_ip, length)) if ET else None
        return False
