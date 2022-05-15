from __future__ import annotations

import re
import glob
import time
import pathlib
import typing as t
from securosurf.session_configuration_manager import LiveSessionConfiguration
from securosurf.session_configuration_manager import LiveSessionConfigurationFromLocalFile

########################################################################################################################

class CLASS:
    def __init__(self, root: pathlib.Path):
        self.__last_checked: float = 0.0

        self.__root: pathlib.Path = root

        self.__crew_file_pattern: re.Pattern[t.AnyStr] = re.compile(r'^session\.crew\.([a-z0-9-]{3,})\.json$')
        self.__crews: dict[str, LiveSessionConfiguration.CLASS] = {}
        self.__crew_names: list[str] = []

        self.__builtins: dict[str, LiveSessionConfiguration.CLASS] = {}
        self.__make_builtin("Normal")
        self.__make_builtin("Solo")
        self.__make_builtin("LAN")
        self.__make_builtin("Dynamic")
        self.__builtin_names: list[str] = list(set(self.__builtins.keys()))

    def __make_builtin(self, name: str) -> None:
        self.__builtins[name] = LiveSessionConfigurationFromLocalFile.CLASS(
            self.__root, f"session.{name.lower()}.json", name
        )

    def get_by_name(self, name: str) -> LiveSessionConfiguration.CLASS | None:
        builtin = self.__builtins.get(name, None)
        return self.__crews.get(name, None) if builtin is None else builtin

    def get_all_names(self) -> list[str]:
        return self.__builtin_names + self.get_crew_names()

    def get_builtin_names(self) -> list[str]:
        return self.__builtin_names

    def get_crew_names(self) -> list[str]:
        elapsed = time.time() - self.__last_checked
        if elapsed < 10: return self.__crew_names

        changed = False

        new_crews: dict[str, LiveSessionConfiguration.CLASS] = {}
        for local_crew_file in glob.glob('session.crew.*.json', root_dir=self.__root):
            crew_file_match = self.__crew_file_pattern.match(local_crew_file)
            if crew_file_match is None: continue

            # Fetch the local crews
            crew_name = "[L] " + crew_file_match[1].replace("-", " ").title()
            if crew_name in self.__crews:
                new_crews[crew_name] = self.__crews[crew_name]
            else:
                changed = True
                new_crews[crew_name] = LiveSessionConfigurationFromLocalFile.CLASS(self.__root, local_crew_file, crew_name)

            # TODO fetch the name of the remote crews

        if changed or (len(self.__crews) != len(new_crews)):
            print("Updated the local and remote crew lists.")

        self.__last_checked = time.time()
        self.__crews = new_crews
        self.__crew_names = sorted(list(set(self.__crews.keys())))
        return self.__crew_names
