from __future__ import annotations

import dataclasses as dc

########################################################################################################################

@dc.dataclass(frozen=True)
class CLASS(object):
    IPs: dict[str, str]
    allow_LAN_IPs: bool
    IP_changed: bool
