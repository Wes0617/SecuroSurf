from __future__ import annotations

from securosurf.telemetry import PacketInbound

########################################################################################################################

class CLASS(PacketInbound.CLASS):
    def __init__(
        self,
        local_IP: str,
        local_port: int,
        remote_IP: str,
        remote_port: int,
        size: int,
        identity: str
    ):
        super().__init__(local_IP, local_port, remote_IP, remote_port, size)
        self.identity: str = identity
