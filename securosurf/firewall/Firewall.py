from __future__ import annotations

import time
import pydivert
import threading as t
import collections as c
import multiprocessing as m
from pydivert.packet import Packet

from securosurf.firewall import is_T2_IP
from securosurf.firewall import is_LAN_IP
from securosurf.telemetry import PacketInboundT2Throttled

from securosurf.telemetry_manager import TelemetryManager
from securosurf.process_messaging import ProcessMessaging
from securosurf.session_configuration import SessionConfiguration

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
        self.__messaging: ProcessMessaging.CLASS = messaging
        self.__telemetry_manager = telemetry_manager
        self.__process: m.Process = m.Process(target=self._run, daemon=True)
        self.__session_configuration = initial_session_configuration

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

        self.T2_packet_throttling_deque = c.deque()
        packet_filter = "inbound and udp.DstPort == 6672 and udp.PayloadLength > 0 and ip"
        with pydivert.WinDivert(packet_filter) as win_divert:
            for packet in win_divert:
                if self.__do_allow(packet):
                    win_divert.send(packet)

    def __do_allow(self, packet: Packet):
        ET = True # enable telemetry
        SC = self.__session_configuration
        TM = self.__telemetry_manager
        TM.activity = time.time()
        T2PTQ = self.T2_packet_throttling_deque
        my_ip = packet.dst_addr if packet.is_inbound else packet.src_addr
        rm_ip = packet.dst_addr if packet.is_outbound else packet.src_addr

        if is_T2_IP.FUNC(rm_ip):
            length = len(packet.payload)

            if length in SC.T2_heartbeat_sizes:
                TM.add(PacketInboundT2Heartbeat.CLASS(my_ip, rm_ip, len(packet.payload))) if ET else None
                return True

            TM.host_activity = time.time()

            if SC.T2_packet_throttling is not None:
                now = time.time()
                begin_of_time_frame_time = now - SC.T2_packet_throttling.per_seconds
                while len(T2PTQ) > 0:
                    is_oldest_packet_out_of_time_frame = T2PTQ[0] < begin_of_time_frame_time
                    if is_oldest_packet_out_of_time_frame:
                        T2PTQ.popleft()
                    else:
                        break
                queue_is_full = len(T2PTQ) >= SC.T2_packet_throttling.max_packets
                if queue_is_full:
                    TM.add(PacketInboundT2Throttled.CLASS(my_ip, rm_ip, len(packet.payload))) if ET else None
                    return False
                T2PTQ.append(now)

            TM.add(PacketInboundT2.CLASS(my_ip, rm_ip, len(packet.payload))) if ET else None
            return True

        if SC.allow_list is None:
            TM.add(PacketInboundAllowedStranger.CLASS(my_ip, rm_ip, len(packet.payload))) if ET else None
            return True
        else:
            if SC.allow_list.allow_LAN_IPs is True and is_LAN_IP.FUNC(rm_ip):
                TM.add(PacketInboundAllowListLAN.CLASS(my_ip, rm_ip, len(packet.payload))) if ET else None
                return True

            allow_list_message = SC.allow_list.IPs.get(rm_ip, None)
            if allow_list_message is not None:
                TM.add(PacketInboundAllowList.CLASS(my_ip, rm_ip, len(packet.payload), allow_list_message)) if ET else None
                return True

            TM.add(PacketInboundStranger.CLASS(my_ip, rm_ip, len(packet.payload))) if ET else None
            return False
