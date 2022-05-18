from __future__ import annotations

import dataclasses as dc

########################################################################################################################

@dc.dataclass(frozen=True)
class CLASS(object):
    max_packets: int
    per_seconds: int
