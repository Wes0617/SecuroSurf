from __future__ import annotations

import pathlib as p
from securosurf.session_configuration_manager import LiveSessionConfiguration

########################################################################################################################

JSONString = str
ErrorString = str

class CLASS(LiveSessionConfiguration.CLASS):
    def __init__(self, app_root: p.Path, session_configuration_name: str, filename: str):
        super().__init__(app_root, session_configuration_name, 5)
        self.__filename: str = filename
        self.__path: p.Path = app_root / filename

    def _get_JSON(self) -> tuple[JSONString | None, ErrorString | None]:
        try:
            with open(self.__path, "r") as JSON_file_pointer:
                return JSON_file_pointer.read(), None
        except FileNotFoundError as exception:
            return None, str(__class__) + " " + str(exception)
