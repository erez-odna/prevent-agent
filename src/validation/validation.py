import json
from functools import wraps
from flask import request
from jsonschema import validate, ValidationError
from werkzeug.exceptions import BadRequest
from utils.paths import DataPaths
from utils.file_utils import read_from_file


def load_schema(schema_name):
    schema_file = DataPaths.get_schema_file(schema_name)
    content = read_from_file(schema_file)
    return json.loads(content)


def raw_validate_schema(req, schema_json):
    try:
        validate(req, load_schema(schema_json))
    except ValidationError as e:
        raise BadRequest(e.message) from e


# decorator for validating a request using a schema
def validate_schema(schema_name):
    def validation_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            req = request.get_json()
            raw_validate_schema(req, schema_name)
            return func(*args, **kwargs)

        return wrapped_function

    return validation_decorator
