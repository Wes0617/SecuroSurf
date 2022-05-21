from __future__ import annotations

import pathlib as p

########################################################################################################################

_root = p.Path(__file__).parent.parent

class CLASS:
    application_name: str = "SecuroSurf"
    application_version: str = "2.0.0"
    application_full_name: str = "SecuroSurf 2.0.0"
    application_mime: str = "application/securosurf-2"
    errors_path = _root / "errors"
    configs_path = _root / "configs"
    remote_crews_path = _root / "configs" / "session.crews-remote.json"
    icon_path = _root / "images" / "icon.ico"
    asset_directories_filenames = ["errors", "configs", "images"]

########################################################################################################################

VAR = CLASS()
