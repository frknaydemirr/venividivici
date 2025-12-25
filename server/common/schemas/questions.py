get_question_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "question-id": {"type": "integer", "minimum": 1},
        "question-title": {"type": "string", "maxLength": 150},
        "question-body": {"type": "string", "maxLength": 5000},
        "username": {"type": "string", "maxLength": 32},
        "creation-time": {"type": "string", "format": "date-time"},
        "city-id": {"type": "integer", "minimum": 1},
        "country-id": {"type": "integer", "minimum": 1}
    },
    "required": ["question-id", "question-title", "question-body", "username", "creation-time", "city-id", "country-id"],
    "additionalProperties": False
}

post_question_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "city-id": {"type": "integer", "minimum": 1},
        "question-title": {"type": "string", "maxLength": 150},
        "question-body": {"type": "string", "maxLength": 5000},
        "category-ids": {
            "type": "array",
            "items": {"type": "integer", "minimum": 1}
        }
    },
    "required": ["city-id", "question-title", "question-body", "category-ids"],
    "additionalProperties": False
}

get_new_question_id_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "question-id": {"type": "integer", "minimum": 1}
    },
    "required": ["question-id"],
    "additionalProperties": False
}

get_multiple_questions_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": get_question,
    "additionalProperties": False
}

get_question_counts_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "answer-count": {"type": "integer", "minimum": 0},
        "reply-count": {"type": "integer", "minimum": 0}
    },
    "required": ["answer-count", "reply-count"],
    "additionalProperties": False
}