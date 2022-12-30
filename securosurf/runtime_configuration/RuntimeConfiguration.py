from __future__ import annotations

import dataclasses as dc

########################################################################################################################

@dc.dataclass(frozen=True)
class CLASS:
    tinfoil_hat_mode: bool = False

    def __eq__(self, other) -> bool:
        return \
            isinstance(other, CLASS) and \
            self.tinfoil_hat_mode == other.tinfoil_hat_mode

