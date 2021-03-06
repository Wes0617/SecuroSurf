from __future__ import annotations

from securosurf.firewall import is_LAN_IP

########################################################################################################################

def FUNC(IP: str) -> str:
    if is_LAN_IP.FUNC(IP):
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
    show_piece_1 = total % 4
    show_piece_2 = (total + 1) % 4

    obfuscated_pieces[show_piece_1] = pieces[show_piece_1]
    obfuscated_pieces[show_piece_2] = pieces[show_piece_2]

    return ".".join(obfuscated_pieces)
