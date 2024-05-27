from functools import wraps
from typing import Callable

from flask import request, jsonify, Response


def validate_request_params(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response:
        # get request body params
        data: dict = request.json
        # define valid params
        valid_params = {'title', 'description'}
        # check if request body params has extra keys (params)
        if not set(data.keys()).issubset(valid_params):
            return jsonify({"error": "invalid keys"})
        # also check for extra keys (params)
        if len(data) > 2:
            return jsonify({"error": "too many keys"})
        title, description = data.get('title'), data.get('description')
        # title can't be empty ({"title": ""})
        if title == '':
            return jsonify({"error": "title cannot be empty"})
        # for created case, check title in params
        if request.method == 'POST':
            if not title:
                return jsonify({"error": "title cannot be empty"})
        # check for title length
        if title:
            if len(title) > 32:
                return jsonify({"error": "title too long"})
        # passing through if OK
        return func(*args, **kwargs)
    return wrapper
