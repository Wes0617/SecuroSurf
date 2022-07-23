from __future__ import annotations

import dataclasses as dc

########################################################################################################################

@dc.dataclass(frozen=True)
class CLASS:
    job_mode: bool = False

    def __eq__(self, other) -> bool:
        return \
            isinstance(other, CLASS) and \
            self.job_mode == other.job_mode

