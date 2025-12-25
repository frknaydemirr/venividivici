get_city_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "city-id": {"type": "integer", "minimum": 1},
        "city-name": {"type": "string", "maxLength": 256},
        "url": {"type": "string", "format": "uri"},
        "info": {"type": "string", "maxLength": 10000}
    },
    "required": ["city-id", "city-name"],
    "additionalProperties": False
}

get_multiple_cities_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": get_city,
    "additionalProperties": False
}

get_multiple_cities_short_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "city-id": {"type": "integer", "minimum": 1},
            "city-name": {"type": "string", "maxLength": 256}
        },
        "required": ["city-id", "city-name"]
    },
    "additionalProperties": False
}
