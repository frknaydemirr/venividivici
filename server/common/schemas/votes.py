get_vote_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "vote-type": {"type": "boolean"}
    },
    "required": ["vote-type"],
    "additionalProperties": False
}

post_vote_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "vote-type": {"type": "boolean"}
    },
    "required": ["vote-type"],
    "additionalProperties": False
}