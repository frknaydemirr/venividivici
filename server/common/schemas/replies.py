get_reply_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "reply-id": {"type": "integer", "minimum": 1},
        "answer-id": {"type": "integer", "minimum": 1},
        "username": {"type": "string", "maxLength": 32},
        "reply-body": {"type": "string", "maxLength": 2500},
        "creation-time": {"type": "string", "format": "date-time"}
    },
    "required": ["reply-id", "answer-id", "username", "reply-body", "creation-time"],
    "additionalProperties": False
}

post_reply_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "answer-id": {"type": "integer", "minimum": 1},
        "reply-body": {"type": "string", "maxLength": 2500}
    },
    "required": ["answer-id", "reply-body"],
    "additionalProperties": False
}

get_new_reply_id_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "reply-id": {"type": "integer", "minimum": 1}
    },
    "required": ["reply-id"],
    "additionalProperties": False
}

get_multiple_replies_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": get_reply,
    "additionalProperties": False
}

get_reply_counts_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "vote-count": {"type": "integer"}
    },
    "required": ["vote-count"],
    "additionalProperties": False
}