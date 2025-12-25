get_user_info_schema_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "username": {"type": "string", "maxLength": 150},
        "creation-time": {"type": "string", "format": "date-time"},
        "city-id": {"type": "integer", "minimum": 1}
    },
    "required": ["username", "creation-time", "city-id"],
}

post_user_registration_schema_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "username": {"type": "string", "maxLength": 150},
        "password": {"type": "string", "minLength": 8, "maxLength": 128},
        "city-id": {"type": "integer", "minimum": 1},
        "e-mail-addr": {"type": "string", "format": "email"},
        "full-name": {"type": "string", "maxLength": 64}
    },
    "required": ["username", "password", "e-mail-addr"],
    "additionalProperties": False
}