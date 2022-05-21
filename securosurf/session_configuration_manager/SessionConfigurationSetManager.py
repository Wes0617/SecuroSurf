from __future__ import annotations

import json
import re
import glob
import time
import typing as t
from securosurf.session_configuration_manager import SessionConfigurationManager
from securosurf.session_configuration_manager import SessionConfigurationManagerLocal
from securosurf.session_configuration_manager import SessionConfigurationManagerRemote
from securosurf import information

########################################################################################################################

class CLASS:
    def __init__(self):
        self.__last_checked: float = 0.0

        self.__crew_file_pattern: re.Pattern[t.AnyStr] = re.compile(r'^session\.crew\.([a-zA-Z0-9 ]{3,})\.json$')
        self.__crews: dict[str, SessionConfigurationManager.CLASS] = {}
        self.__crew_names: list[str] = []

        self.__builtins: dict[str, SessionConfigurationManager.CLASS] = {}
        self.__make_builtin("Normal")
        self.__make_builtin("Solo")
        self.__make_builtin("LAN")
        self.__make_builtin("Dynamic")
        self.__builtin_names: list[str] = list(set(self.__builtins.keys()))

    def __make_builtin(self, name: str) -> None:
        self.__builtins[name] = SessionConfigurationManagerLocal.CLASS(f"session.{name.lower()}.json", name)

    def get_by_name(self, name: str) -> SessionConfigurationManager.CLASS | None:
        builtin = self.__builtins.get(name, None)
        return self.__crews.get(name, None) if builtin is None else builtin

    def get_all_names(self) -> list[str]:
        return self.__builtin_names + self.get_crew_names()

    def get_builtin_names(self) -> list[str]:
        return self.__builtin_names

    def get_crew_names(self) -> list[str]:
        elapsed = time.time() - self.__last_checked
        if elapsed < 10: return self.__crew_names

        new_crews: dict[str, SessionConfigurationManager.CLASS] = {}
        for local_crew_filename in glob.glob('session.crew.*.json', root_dir=information.VAR.configs_path):
            crew_file_match = self.__crew_file_pattern.match(local_crew_filename)
            if crew_file_match is None: continue
            crew_name = "[L] " + crew_file_match[1]
            if crew_name in self.__crews:
                new_crews[crew_name] = self.__crews[crew_name]
            else:
                new_crews[crew_name] = SessionConfigurationManagerLocal.CLASS(local_crew_filename, crew_name)

        if information.VAR.remote_crews_path.exists():
            try:
                with open(information.VAR.remote_crews_path, "r") as fp:
                    remote_crews_JSON = fp.read()
                    JSON_object = json.loads(remote_crews_JSON)
                    for crew_name_no_prefix in JSON_object:
                        crew_name = "[R] " + crew_name_no_prefix
                        URL = JSON_object[crew_name_no_prefix]
                        if crew_name in self.__crews:
                            new_crews[crew_name] = self.__crews[crew_name]
                        else:
                            new_crews[crew_name] = SessionConfigurationManagerRemote.CLASS(crew_name, URL)
            except Exception as exception:
                print(exception)

        self.__last_checked = time.time()
        self.__crews = new_crews
        self.__crew_names = sorted(list(set(self.__crews.keys())))
        return self.__crew_names
