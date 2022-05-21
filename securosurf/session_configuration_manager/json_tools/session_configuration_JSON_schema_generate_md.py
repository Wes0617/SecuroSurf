from __future__ import annotations

import json
from securosurf import information
from securosurf.session_configuration_manager.json_tools import session_configuration_JSON_schema

########################################################################################################################

def FUNC() -> None:
    __destination = information.VAR.configs_path / "session_configuration_json_schema.md"
    with open(__destination, "w+") as __file_pointer:
        __file_pointer.write("# Session Configuration JSON Schema\n\n")
        __file_pointer.write("```json\n")
        json.dump(session_configuration_JSON_schema.VAR, fp=__file_pointer, indent="\t", separators=(",", ": "))
        __file_pointer.write("\n```\n")
