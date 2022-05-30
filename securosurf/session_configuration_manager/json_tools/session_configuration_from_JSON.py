from __future__ import annotations

import json
import jsonschema.exceptions as jse
from securosurf.session_configuration import SessionConfiguration
from securosurf.session_configuration import SessionConfigurationAllowList
from securosurf.session_configuration import SessionConfigurationSessionLock
from securosurf.session_configuration import SessionConfigurationT2Throttling
from securosurf.session_configuration_manager.json_tools import session_configuration_validate_normalize_JSON

########################################################################################################################

ErrorString = str

def FUNC(JSON: str, fetch_time_if_success: float) -> tuple[SessionConfiguration.CLASS | None, ErrorString | None]:
    try:
        JSON_object = json.loads(JSON)
        session_configuration_validate_normalize_JSON.FUNC(JSON_object)
    except (json.JSONDecodeError, jse.ValidationError) as exception:
        return None, str(exception)

    T2H = set(JSON_object.get("T2_heartbeat_sizes"))

    v = JSON_object.get("T2_throttling", None)
    T2T = None if v is None else SessionConfigurationT2Throttling.CLASS(v["max_packets"], v["per_seconds"])

    v = JSON_object.get("allow_list", None)
    AL = None if v is None else SessionConfigurationAllowList.CLASS(v["IPs"], v["allow_LAN_IPs"], v["IP_changed"])

    v = JSON_object.get("session_lock", None)
    SL = None if v is None else SessionConfigurationSessionLock.CLASS(v["default_enabled"])

    return SessionConfiguration.CLASS(
        fetch_time=fetch_time_if_success,
        welcome_message=JSON_object["welcome_message"],
        update_frequency=JSON_object["update_frequency"],
        T2_heartbeat_sizes=T2H,
        T2_throttling=T2T,
        allow_list=AL,
        session_lock=SL
    ), None
