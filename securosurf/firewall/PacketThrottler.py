from __future__ import annotations

import time
import collections as c

########################################################################################################################

class CLASS:
    def __init__(self):
        self.__deque = c.deque()

    def do_throttle(self, seconds: int, max_packets: int) -> bool:
        now = time.time()

        begin_of_time_frame_time = now - seconds
        while len(self.__deque) > 0:
            is_oldest_packet_out_of_time_frame = self.__deque[0] < begin_of_time_frame_time
            if is_oldest_packet_out_of_time_frame:
                self.__deque.popleft()
            else:
                break

        queue_is_full = len(self.__deque) >= max_packets

        if not queue_is_full:
            self.__deque.append(now)

        return queue_is_full
