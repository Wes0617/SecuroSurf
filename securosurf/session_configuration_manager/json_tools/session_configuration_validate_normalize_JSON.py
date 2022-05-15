from __future__ import annotations

import typing as t
import jsonschema as jss
from jsonschema import validators as jssv
from securosurf.session_configuration_manager.json_tools import session_configuration_JSON_schema

########################################################################################################################

def FUNC(JSON: t.Any) -> None:
    validator_class = jss.Draft7Validator
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for prop, sub_schema in properties.items():
            if "default" in sub_schema:
                instance.setdefault(prop, sub_schema["default"])
        for error in validate_properties(validator, properties, instance, schema):
            yield error

    ExtendedValidator = jssv.extend(validator_class, {"properties": set_defaults})
    ExtendedValidator(session_configuration_JSON_schema.VAR).validate(JSON)
