from __future__ import annotations

import time
import collections as c
import dataclasses as dc
from securosurf.telemetry_manager import LiveTraffic

########################################################################################################################

_active_max_age_minutes = 2

_host_max_age_minutes = 3

@dc.dataclass(frozen=True)
class CLASS:
    traffic: c.deque[LiveTraffic.CLASS]

    last_activity: float | None

    last_host_activity: float | None

    # ------------------------------------------------------------------------------------------------------------------

    @property
    def has_activity(self) -> bool:
        return self.last_activity is not None

    @property
    def last_activity_age(self) -> float | None:
        return time.time() - self.last_activity if self.has_activity else None

    @property
    def is_active(self) -> bool:
        return self.has_activity and self.last_activity_age < (_active_max_age_minutes * 60)

    # ------------------------------------------------------------------------------------------------------------------

    @property
    def has_host_activity(self) -> bool:
        return self.last_host_activity is not None

    @property
    def last_host_activity_age(self) -> float | None:
        return time.time() - self.last_host_activity if self.has_host_activity else None

    @property
    def is_hosting(self) -> bool:
        return self.has_host_activity and self.last_host_activity_age < (_host_max_age_minutes * 60)
