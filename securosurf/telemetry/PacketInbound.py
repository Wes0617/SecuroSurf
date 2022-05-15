from __future__ import annotations

from securosurf.telemetry import Packet

########################################################################################################################

class CLASS(Packet.CLASS):
    def __init__(
        self,
        local_IP: str,
        remote_IP: str,
        size: int,
    ):
        super().__init__(local_IP, remote_IP, True, size)
