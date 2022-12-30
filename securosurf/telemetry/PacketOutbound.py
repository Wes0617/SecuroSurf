from __future__ import annotations

from securosurf.telemetry import Packet

########################################################################################################################

class CLASS(Packet.CLASS):
    def __init__(
        self,
        local_IP: str,
        local_port: int,
        remote_IP: str,
        remote_port: int,
        size: int,
    ):
        super().__init__(local_IP, local_port, remote_IP, remote_port, False, size)
