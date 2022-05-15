from __future__ import annotations

from securosurf.firewall import is_T2_IP

########################################################################################################################

def FUNC(IP: str) -> str:
    if is_T2_IP.FUNC(IP):
        return IP

    # Obfuscate the IP in a predictable manner,
    # ie the same IP will be obfuscated the same in all the instances of the firewall
    pieces = IP.split(".")
    obfuscated_pieces = ["┉"] * 4

    p1 = int(pieces[0])
    p2 = int(pieces[1]) * 2
    p3 = int(pieces[2]) * 3
    p4 = int(pieces[3]) * 4
    total = p1 + p2 + p3 + p4
    show_piece = total % 4

    obfuscated_pieces[show_piece] = pieces[show_piece]

    return ".".join(obfuscated_pieces)
