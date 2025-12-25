from jsonschema import validate
from sanic import exceptions

def check_schema(data: dict, schema: dict):
    try:
        validate(instance=data, schema=schema)
    except:
        raise exceptions.InvalidUsage("Invalid request JSON.")