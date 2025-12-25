post_city_sub_unsub_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "city-id": {"type": "integer", "minimum": 1},
        "subscription-type": {"type": "boolean"}
    },
    "required": ["city-id", "subscription-type"],
    "additionalProperties": False
}

post_country_sub_unsub_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "country-id": {"type": "integer", "minimum": 1},
        "subscription-type": {"type": "boolean"}
    },
    "required": ["country-id", "subscription-type"],
    "additionalProperties": False
}