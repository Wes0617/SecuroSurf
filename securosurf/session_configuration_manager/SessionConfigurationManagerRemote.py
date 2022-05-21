from __future__ import annotations

import requests
import pathlib as p
from base64 import b64decode
from Crypto.Cipher import AES
from securosurf import information
from Crypto.Util.Padding import unpad
from securosurf.session_configuration_manager import SessionConfigurationManager

########################################################################################################################

JSONString = str
ErrorString = str

class CLASS(SessionConfigurationManager.CLASS):
    def __init__(self, app_root: p.Path, session_configuration_name: str, URL: str):
        super().__init__(app_root, session_configuration_name, 30)
        self.__URL: str = URL

    def _get_JSON(self) -> tuple[JSONString | None, ErrorString | None]:
        try:
            print("Requesting session configuration from remote")
            headers = {"Accept": information.VAR.application_mime}
            result = requests.get(url=self.__URL, headers=headers)
            if result.status_code != 200:
                raise Exception()
            pp = b'Lester Crest'.ljust(32, b'\0')
            aes = AES.new(pp, AES.MODE_CBC, b'Office Assistant')
            JSON = aes.decrypt(b64decode(result.content))
            JSON = unpad(JSON, AES.block_size)
            JSON = JSON.decode('UTF-8')
            return JSON, None
        except Exception as exception:
            return None, str(exception)
