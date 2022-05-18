from __future__ import annotations

import time
import dataclasses as dc
from securosurf.session_configuration import SessionConfigurationAllowList
from securosurf.session_configuration import SessionConfigurationSessionLock
from securosurf.session_configuration import SessionConfigurationT2Throttling

########################################################################################################################

@dc.dataclass(frozen=True)
class CLASS:

    welcome_message: str

    update_frequency: int

    T2_heartbeat_sizes: set[int] = dc.field(default_factory=set, init=True)

    T2_throttling: SessionConfigurationT2Throttling.CLASS | None = None

    allow_list: SessionConfigurationAllowList.CLASS | None = None

    session_lock: SessionConfigurationSessionLock.CLASS | None = None

    fetch_time: float = dc.field(default_factory=time.time, init=False)

    def __eq__(self, other) -> bool:
        return \
            isinstance(other, CLASS) and \
            self.welcome_message == other.welcome_message and \
            self.update_frequency == other.update_frequency and \
            self.T2_heartbeat_sizes == other.T2_heartbeat_sizes and \
            self.T2_throttling == other.T2_throttling and \
            self.allow_list == other.allow_list and \
            self.session_lock == other.session_lock

