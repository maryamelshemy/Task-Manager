from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

MANAGER_ROLE_ID = 1


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return fn(*args, **kwargs)
    return wrapper


def manager_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role_id") != MANAGER_ROLE_ID:
            return jsonify({"error": "Manager access required"}), 403
        return fn(*args, **kwargs)
    return wrapper