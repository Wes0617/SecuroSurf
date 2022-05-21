from __future__ import annotations

import collections as c
from securosurf.telemetry import Packet
from securosurf.telemetry import PacketInboundT2
from securosurf.telemetry import PacketInboundStranger
from securosurf.telemetry import PacketInboundAllowList
from securosurf.telemetry import PacketInboundT2Heartbeat
from securosurf.telemetry import PacketInboundT2Throttled
from securosurf.telemetry import PacketInboundAllowListLAN
from securosurf.telemetry import PacketInboundAllowedStranger
from securosurf.telemetry_manager import LiveTraffic
from securosurf.telemetry_manager import Telemetry

########################################################################################################################

class CLASS:
    def __init__(self, log_size: int):
        self.__slots: dict[str, LiveTraffic.CLASS] = {}
        self.__log: c.deque[LiveTraffic.CLASS] = c.deque(maxlen=log_size)
        self.activity: float | None = None
        self.host_activity: float | None = None

    def add(self, packet: Packet.CLASS):
        if isinstance(packet, PacketInboundT2Heartbeat.CLASS):
            self.__slots.clear()
            self.__log.append(LiveTraffic.CLASS(packet))
        elif isinstance(packet, PacketInboundT2Throttled.CLASS):
            self.__slots.clear()
            self.__log.append(LiveTraffic.CLASS(packet))
        elif isinstance(packet, PacketInboundT2.CLASS):
            self.__add_slotted(f"T2", packet)

        elif isinstance(packet, PacketInboundAllowList.CLASS):
            packet: PacketInboundAllowList.CLASS # only necessary for autocompletion
            self.__add_slotted(f"AllowList " + packet.identity, packet)
        elif isinstance(packet, PacketInboundAllowListLAN.CLASS):
            self.__add_slotted(f"AllowListLAN", packet)
        elif isinstance(packet, PacketInboundStranger.CLASS):
            self.__add_slotted(f"Stranger {packet.remote_IP}", packet)
        elif isinstance(packet, PacketInboundAllowedStranger.CLASS):
            self.__add_slotted(f"AllowedStranger {packet.remote_IP}", packet)

        else:
            raise Exception()

    def __add_slotted(self, slot_name: str, traffic_match: Packet.CLASS):
        existing_slot = self.__slots.get(slot_name, None)
        if existing_slot is None:
            new_slot = LiveTraffic.CLASS(traffic_match)
            self.__slots[slot_name] = new_slot
            self.__log.append(new_slot)
        else:
            existing_slot.repeat(traffic_match)

    def get_telemetry(self) -> Telemetry.CLASS:
        return Telemetry.CLASS(self.__log, self.activity, self.host_activity)
