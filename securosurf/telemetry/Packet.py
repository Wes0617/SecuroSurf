from __future__ import annotations

import abc
import time

########################################################################################################################

class CLASS(abc.ABC):
    def __init__(
        self,
        local_IP: str,
        local_port: int,
        remote_IP: str,
        remote_port: int,
        inbound: bool,
        size: int,
    ):
        self.time: float = time.time()
        self.local_IP: str = local_IP
        self.local_port: int = local_port
        self.remote_IP: str = remote_IP
        self.remote_port: int = remote_port
        self.inbound: bool = inbound
        self.size: int = size
