from __future__ import annotations

import pathlib as p

########################################################################################################################

class CLASS:
    def __init__(self, root: p.Path):
        self.application_name: str = "SecuroSurf"
        self.application_version: str = "2.0.6"
        self.application_full_name: str = "SecuroSurf 2.0.6 Lupe Edition"
        self.application_ID: str = "SecuroSurf"

        self.application_mime: str = "application/securosurf-2"

        self.path: p.Path = root
        self.errors_path: p.Path = root / "errors"
        self.configs_path: p.Path = root / "configs"
        self.remote_crews_path: p.Path = root / "configs" / "session.crews-remote.json"
        self.icon_path: p.Path = root / "images" / "icon.ico"

        self.asset_directories_filenames: list[str] = ["configs", "errors", "images"]

########################################################################################################################

VAR: CLASS | None = None
