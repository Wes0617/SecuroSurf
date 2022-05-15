from __future__ import annotations

import typing as t
import multiprocessing as m

########################################################################################################################

Request = str
Contents = t.Any

class CLASS:
    def __init__(self, to_self: m.Queue, to_other: m.Queue):
        self.__to_self = to_self
        self.__to_other = to_other

    def send_message(self, request: Request, contents: Contents = None):
        self.__to_other.put((request, contents), block=True)

    def receive_message(self) -> tuple[Request, Contents]:
        return self.__to_self.get(block=True)

    def invert(self) -> CLASS:
        return self.__class__(self.__to_other, self.__to_self)
