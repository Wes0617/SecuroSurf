from __future__ import annotations

import dataclasses as dc

########################################################################################################################

@dc.dataclass(frozen=True)
class CLASS:
    locked_mode: bool = False

    def __eq__(self, other) -> bool:
        return \
            isinstance(other, CLASS) and \
            self.locked_mode == other.locked_mode

