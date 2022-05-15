from __future__ import annotations

import re

########################################################################################################################

__T2_IP_pattern = re.compile(r'^(185\.56\.6[4-7]\.\d{1,3})$')

def FUNC(IP: str) -> bool:
    return __T2_IP_pattern.match(IP) is not None
