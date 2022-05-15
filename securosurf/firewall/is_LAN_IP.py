from __future__ import annotations

import socket
import struct

########################################################################################################################

def FUNC(IP) -> bool:
    # https://stackoverflow.com/a/8339939/4251625
    IP_int = struct.unpack('!I', socket.inet_pton(socket.AF_INET, IP))[0]
    networks = (
        # [2130706432, 4278190080],  # 127.0.0.0,   255.0.0.0   https://www.rfc-editor.org/rfc/rfc3330
        [3232235520, 4294901760],  # 192.168.0.0, 255.255.0.0 https://www.rfc-editor.org/rfc/rfc1918
        [2886729728, 4293918720],  # 172.16.0.0,  255.240.0.0 https://www.rfc-editor.org/rfc/rfc1918
        [167772160, 4278190080],   # 10.0.0.0,    255.0.0.0   https://www.rfc-editor.org/rfc/rfc1918
    )
    for network in networks:
        if (IP_int & network[1]) == network[0]:
            return True
    return False
