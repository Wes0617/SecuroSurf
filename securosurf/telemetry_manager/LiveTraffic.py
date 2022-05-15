from __future__ import annotations

from securosurf.telemetry import Packet

########################################################################################################################

class CLASS:
    def __init__(self, packet: Packet.CLASS):
        self.__count: int = 1
        self.__start_packet: Packet.CLASS = packet
        self.__end_packet: Packet.CLASS = packet

    @property
    def count(self) -> int:
        return self.__count

    @property
    def start_packet(self) -> Packet.CLASS:
        return self.__start_packet

    @property
    def end_packet(self) -> Packet.CLASS:
        return self.__end_packet

    def repeat(self, match: Packet.CLASS) -> None:
        self.__count += 1
        self.__end_packet = match
