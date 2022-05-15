from __future__ import annotations

import time
import json
import pathlib
import jsonschema.exceptions as jsse
from securosurf.session_configuration import SessionConfiguration
from securosurf.session_configuration_manager import LiveSessionConfiguration
from securosurf.session_configuration_manager.json_tools import session_configuration_from_JSON

########################################################################################################################

class CLASS(LiveSessionConfiguration.CLASS):
    def __init__(self, parent_path: pathlib.Path, filename: str, name: str):
        self.__filename: str = filename
        self.__path: pathlib.Path = parent_path / filename
        self.__error_filename = filename + ".error.txt"
        self.__error_path: pathlib.Path = parent_path / self.__error_filename
        self.__latest_update_attempt: float = 0
        self.__name: str = name
        self.__session_configuration: SessionConfiguration.CLASS = SessionConfiguration.CLASS(
            welcome_message=f"Error! Check the file \"{self.__error_filename}\" for more info.",
            update_frequency=5,
        )

    @property
    def latest_update_attempt(self) -> float | None:
        return None if self.__latest_update_attempt == 0 else self.__latest_update_attempt

    def get(self) -> SessionConfiguration.CLASS:
        elapsed = time.time() - self.__latest_update_attempt
        if elapsed < self.__session_configuration.update_frequency:
            return self.__session_configuration

        self.__latest_update_attempt = time.time()
        new_session_configuration = self.__fetch_from_file()
        if isinstance(new_session_configuration, SessionConfiguration.CLASS):
            self.__session_configuration = new_session_configuration
            print(f"Successfully attempted to update the active session configuration \"{self.__name}\".")
        else:
            with open(self.__error_path, 'w') as file_pointer:
                file_pointer.write(str(new_session_configuration))
            print(f"Error updating the session configuration! Check \"{self.__error_filename}\" for more info.")

        return self.__session_configuration

    def __fetch_from_file(self) -> SessionConfiguration.CLASS | FileNotFoundError | json.JSONDecodeError | jsse.ValidationError:
        try:
            with open(self.__path, "r") as JSON_string_data:
                crew_DTO = json.load(JSON_string_data)
                return session_configuration_from_JSON.FUNC(crew_DTO)
        except (FileNotFoundError, json.JSONDecodeError) as exception:
            return exception
