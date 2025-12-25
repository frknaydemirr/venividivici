get_category_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "category-id": {"type": "integer", "minimum": 1},
        "category-label": {"type": "string", "maxLength": 64}
    },
    "required": ["category-id", "category-label"],
    "additionalProperties": False
}

get_multiple_categories_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": get_category_schema,
    "additionalProperties": False
}

get_multiple_categories_with_stats_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "category-id": {"type": "integer", "minimum": 1},
            "category-label": {"type": "string", "maxLength": 64},
            "question-count": {"type": "integer", "minimum": 0},
            "answer-count": {"type": "integer", "minimum": 0}
        }
    },
    "required": ["category-id", "category-label", "question-count", "answer-count"],
    "additionalProperties": False
}