from __future__ import annotations

import abc
import time
import pathlib as p
from securosurf.session_configuration import SessionConfiguration
from securosurf.session_configuration_manager.json_tools import session_configuration_from_JSON
from securosurf import  information

########################################################################################################################

JSONString = str
ErrorString = str

class CLASS(abc.ABC):

    def __init__(self, crew_name: str, retry_frequency_if_fail: int):
        self.__error_path: p.Path = information.VAR.errors_path / (crew_name + ".txt")
        self.__last_update_attempt: float = 0
        self.__session_configuration: SessionConfiguration.CLASS = SessionConfiguration.CLASS(
            welcome_message=f"Error! Check the \"errors\" folder for more info!",
            update_frequency=retry_frequency_if_fail,
        )

    @property
    def last_update_attempt(self) -> float | None:
        return None if self.__last_update_attempt == 0 else self.__last_update_attempt

    # @final
    def get(self) -> SessionConfiguration.CLASS:
        elapsed = time.time() - self.__last_update_attempt
        if elapsed < self.__session_configuration.update_frequency:
            return self.__session_configuration
        self.__last_update_attempt = time.time()

        JSON, error = self._get_JSON()

        if JSON is not None:
            new_session_configuration, error = session_configuration_from_JSON.FUNC(JSON)
            if new_session_configuration is not None:
                self.__session_configuration = new_session_configuration
                return new_session_configuration

        with open(self.__error_path, 'w') as error_file_pointer:
            error_file_pointer.write(error)
        return self.__session_configuration

    @abc.abstractmethod
    def _get_JSON(self) -> tuple[JSONString | None, ErrorString | None]:
        pass
