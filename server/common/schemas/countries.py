get_country_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "country-id": {"type": "integer", "minimum": 1},
        "country-name": {"type": "string", "maxLength": 256},
        "info": {"type": "string", "maxLength": 10000},
        "url": {"type": "string", "format": "uri"}
    },
    "required": ["country-id", "country-name"],
    "additionalProperties": False
}

get_multiple_countries_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": get_country_schema,
    "additionalProperties": False
}

get_multiple_countries_short_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "country-id": {"type": "integer", "minimum": 1},
            "country-name": {"type": "string", "maxLength": 256}
        },
        "required": ["country-id", "country-name"]
    },
    "additionalProperties": False
}