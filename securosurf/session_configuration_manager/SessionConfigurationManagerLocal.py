from __future__ import annotations

import pathlib as p
from securosurf.session_configuration_manager import SessionConfigurationManager
from securosurf import information

########################################################################################################################

JSONString = str
ErrorString = str

class CLASS(SessionConfigurationManager.CLASS):
    def __init__(self, session_configuration_JSON_filename: str, session_configuration_name: str):
        super().__init__(session_configuration_name, 5)
        self.__path: p.Path = information.VAR.configs_path / session_configuration_JSON_filename

    def _get_JSON(self) -> tuple[JSONString | None, ErrorString | None]:
        try:
            with open(self.__path, "r") as JSON_file_pointer:
                return JSON_file_pointer.read(), None
        except FileNotFoundError as exception:
            return None, str(exception)
