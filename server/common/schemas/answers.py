get_answer_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "answer-id": {"type": "integer", "minimum": 1},
        "question-id": {"type": "integer", "minimum": 1},
        "username": {"type": "string", "maxLength": 32},
        "answer-body": {"type": "string", "maxLength": 2500},
        "creation-time": {"type": "string", "format": "date-time"}
    },
    "required": ["answer-id", "question-id", "username", "answer-body", "creation-time"],
    "additionalProperties": False
}

post_answer_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "question-id": {"type": "integer", "minimum": 1},
        "answer-body": {"type": "string", "maxLength": 2500}
    },
    "required": ["question-id", "answer-body"],
    "additionalProperties": False
}

get_new_answer_id_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "answer-id": {"type": "integer", "minimum": 1}
    },
    "required": ["answer-id"],
    "additionalProperties": False
}

get_multiple_answers_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": get_answer_schema,
    "additionalProperties": False
}

get_answer_counts_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "reply-count": {"type": "integer", "minimum": 0},
        "vote-count": {"type": "integer"}
    },
    "required": ["reply-count", "vote-count"],
    "additionalProperties": False
}