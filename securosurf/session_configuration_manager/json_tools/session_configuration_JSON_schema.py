from __future__ import annotations

########################################################################################################################

VAR = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "description": "Defines the options for a firewalled session type or a GTA Online crew.",
    "type": "object",
    "properties": {
        "welcome_message": {
            "description": "A description of the session configuration, or a welcome message for the people activating "
                           "this crew.",
            "type": "string",
            "minLength": 3,
            "maxLength": 280,
            "default": "Welcome to SecuroSurf! I'll take care of the cheaters, you take care of the company.",
        },

        "update_frequency": {
            "description": "How often the crew definition must be reloaded from the source, be it remote or local. "
                           "For remote crews, this should be set between 15 and 60 seconds. Local crews can be updated "
                           "more frequently because the cost of the request is negligible.",
            "type": "integer",
            "minimum": 5,
            "maximum": 60 * 5,
            "default": 30,
        },

        "T2_heartbeat_sizes": {
            "description": "T2 packets that should be always allowed as they simply check whether the user is still "
                           "online. These should be provided automatically by the program. Only define this property "
                           "if there is an actual reason to do it.",
            "type": "array",
            "items": {
                "type": "integer",
                "minimum": 1,
                "maximum": 2000,
                "maxLength": 20,
            },
            "default": [12, 18],
        },

        "allow_list": {
            "description": "The list of allowed IPs. Omit this property to disable the feature and allow everyone.",
            "type": "object",
            "properties": {
                "IPs": {
                    "description": "Use IPv4 as key, and the in-game name of the player as value. If this object is "
                                   "empty, no one will be allowed in the session (unless they are allowed by the other "
                                   "options, such as \"allow_LAN_IPs\").",
                    "type": "object",
                    "patternProperties": {
                        r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$": {
                            "type": "string",
                            "minLength": 3,
                            "maxLength": 50,
                        },
                    },
                    "additionalProperties": False,
                },

                "allow_LAN_IPs": {
                    "description": "Whether to allow direct connections with other computers in the LAN. There is "
                                   "probably no reason to ever disable this, except for solo sessions. This setting "
                                   "includes the following range: 192.168.0.0/16.",
                    "type": "boolean",
                    "default": True,
                },

                "force_allow_T2_IPs": {
                    "description": "Whether to allow all traffic from T2 IPs. This is not normally something you would "
                                   "do, because it makes tunneling possible, but it is necessary for some special "
                                   "modes of the firewall.",
                    "type": "boolean",
                    "default": False,
                },

                "IP_changed": {
                    "description": "This entry is meant for remote crews only, and it is used to signal that the IP of "
                                   "the crew member performing the request has changed.",
                    "type": "boolean",
                    "default": False,
                },
            },

            "required": ["IPs"],
        },

        "T2_throttling": {
            "description": "Throttle the T2 packets in order to prevent full-blown gameplay connections, while still "
                           "making matchmaking possible. If omitted, all traffic from T2 IPs will be allowed. "
                           "This option has only effect if the \"allow_list\" is enabled.",
            "type": "object",
            "properties": {
                "max_packets": {
                    "description": "The maximum amount of T2 packets allowed in the specified time. "
                                   "If set to 0, all packets will be blocked.",
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 60 * 10 * 2,
                },
                "per_seconds": {
                    "description": "The period of time in which the specified amount of packets will be allowed.",
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 60 * 10,
                },
            },
            "required": ["max_packets", "per_seconds"],
        },

        "strangers_throttling": {
            "description": "Data is regularly exchanged with strangers, even if they are not actually trying to join "
                           "the lobby. This is probably used to test latency, or something like that. Use this option "
                           "to allow this type of minimal packet exchange with strangers, or omit it to block "
                           "everything. This option has effect only if the \"allow_list\" is enabled.",
            "type": "object",
            "properties": {
                "max_packets": {
                    "description": "The maximum amount of packets from strangers allowed in the specified time. "
                                   "If set to 0, all packets will be blocked.",
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 60 * 10 * 2,
                },
                "per_seconds": {
                    "description": "The period of time in which the specified amount of packets will be allowed.",
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 60 * 10,
                },
            },
            "required": ["max_packets", "per_seconds"],
        },

        "session_lock": {
            "description": "Add this entry if the players are allowed to lock their sessions and prevent other people "
                           "in the allow-list to join it. In other words, this allows to create an even stricter "
                           "allow-list. Omit this property if the user should not be allowed to lock their sessions.",
            "type": "object",
            "properties": {
                "default_enabled": {
                    "description": "Whether to enable the session-lock by default.",
                    "type": "boolean",
                    "default": False,
                }
            },
        },
    },
}
