from __future__ import annotations

import time
import collections as c
import dataclasses as dc
from securosurf.telemetry_manager import LiveTraffic

########################################################################################################################

@dc.dataclass(frozen=True)
class CLASS:
    traffic: c.deque[LiveTraffic.CLASS]

    last_activity: float | None

    last_T2_host_packet: float | None

    @property
    def last_activity_age(self) -> float | None:
        return None if self.last_activity is None else time.time() - self.last_activity

    @property
    def last_T2_host_packet_age(self) -> float | None:
        return None if self.last_T2_host_packet is None else time.time() - self.last_T2_host_packet
