from __future__ import annotations

import time
import random
import threading as t
import multiprocessing as m

from securosurf.process_messaging import ProcessMessaging
from securosurf.session_configuration import SessionConfiguration
from securosurf.telemetry import PacketInboundStranger
from securosurf.telemetry import PacketInboundAllowList
from securosurf.telemetry import PacketInboundT2
from securosurf.telemetry import PacketInboundT2Heartbeat
from securosurf.telemetry import PacketInboundAllowListLAN
from securosurf.telemetry_manager import TelemetryManager

########################################################################################################################

# Generates random traffic logs. Only used for testing.
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
        self.__process.start()

    def stop(self):
        self.__process.terminate()

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

        while True:
            packet_size = random.randint(25, 400)
            packet_type = random.randint(1, 100_000)
            if packet_type <= 10:
                match = PacketInboundT2Heartbeat.CLASS("192.168.1.55", "185.56.65.170", 12)
            elif packet_type <= 20:
                match = PacketInboundT2.CLASS("192.168.1.55", "185.56.65.170", packet_size)
            elif packet_type <= 1000:
                match = PacketInboundStranger.CLASS("192.168.1.55", "185.56.65.170", packet_size)
            else:
                if random.randint(0, 3) == 0:
                    match = PacketInboundAllowListLAN.CLASS("192.168.1.55", "185.56.65.170", packet_size)
                else:
                    identity = ["Franklin", "Michael", "Trevor"][random.randint(0, 2)]
                    match = PacketInboundAllowList.CLASS("192.168.1.55", "185.56.65.170", packet_size, identity)
            self.__telemetry_manager.add(match)
            time.sleep(0.0001)
