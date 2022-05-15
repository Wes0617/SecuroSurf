from __future__ import annotations

import abc
import time

########################################################################################################################

class CLASS(abc.ABC):
    def __init__(
        self,
        local_IP: str,
        remote_IP: str,
        inbound: bool,
        size: int,
    ):
        self.time: float = time.time()
        self.local_IP: str = local_IP
        self.remote_IP: str = remote_IP
        self.inbound: bool = inbound
        self.size: int = size
