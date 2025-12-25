get_qa_counts_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "question-count": {"type": "integer", "minimum": 0},
        "answer-count": {"type": "integer", "minimum": 0}
    },
    "required": ["question-count", "answer-count"],
    "additionalProperties": False
}