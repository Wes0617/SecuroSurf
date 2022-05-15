from __future__ import annotations

from securosurf.telemetry import PacketInbound

########################################################################################################################

class CLASS(PacketInbound.CLASS):
    def __init__(
        self,
        local_IP: str,
        remote_IP: str,
        size: int,
        identity: str
    ):
        super().__init__(local_IP, remote_IP, size)
        self.identity: str = identity
