from __future__ import annotations

import abc
from securosurf.session_configuration import SessionConfiguration

########################################################################################################################

class CLASS(abc.ABC):
    @abc.abstractmethod
    def get(self) -> SessionConfiguration.CLASS:
        pass

    @property
    @abc.abstractmethod
    def latest_update_attempt(self) -> float | None:
        pass
