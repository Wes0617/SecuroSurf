from __future__ import annotations

import json
import jsonschema.exceptions as jse
from securosurf.session_configuration import SessionConfiguration
from securosurf.session_configuration import SessionConfigurationAllowList
from securosurf.session_configuration import SessionConfigurationSessionLock
from securosurf.session_configuration import SessionConfigurationT2PacketThrottling
from securosurf.session_configuration import SessionConfigurationT2MandatoryPacketDetection
from securosurf.session_configuration_manager.json_tools import session_configuration_validate_normalize_JSON

########################################################################################################################

ErrorString = str

def FUNC(JSON: str) -> tuple[SessionConfiguration.CLASS | None, ErrorString | None]:
    try:
        JSON_object = json.loads(JSON)
        session_configuration_validate_normalize_JSON.FUNC(JSON_object)
    except (json.JSONDecodeError, jse.ValidationError) as exception:
        return None, str(exception)

    T2_HB = set(JSON_object.get("T2_heartbeat_sizes"))

    v = JSON_object.get("T2_packet_throttling", None)
    T2_PT = None if v is None else SessionConfigurationT2PacketThrottling.CLASS(v["max_packets"], v["per_seconds"])

    v = JSON_object.get("T2_mandatory_packet_detection", None)
    T2_MP = None if v is None else SessionConfigurationT2MandatoryPacketDetection.CLASS(v["max_repeats"])

    v = JSON_object.get("allow_list", None)
    AL = None if v is None else SessionConfigurationAllowList.CLASS(v["IPs"], v["allow_LAN_IPs"])

    v = JSON_object.get("session_lock", None)
    SL = None if v is None else SessionConfigurationSessionLock.CLASS(v["default_enabled"])

    return SessionConfiguration.CLASS(
        welcome_message=JSON_object["welcome_message"],
        update_frequency=JSON_object["update_frequency"],
        T2_heartbeat_sizes=T2_HB,
        T2_packet_throttling=T2_PT,
        T2_mandatory_packet_detection=T2_MP,
        allow_list=AL,
        session_lock=SL
    ), None
