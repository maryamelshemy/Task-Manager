import secrets
from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

from extensions import db
from models.employee import Employee
from models.password_reset import PasswordReset
from utils.email_utils import send_reset_email

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    employee = Employee.query.filter_by(email=email).first()

    if not employee:
        print("Employee not found")
        return jsonify({"error": "Invalid email or password"}), 401

    print("Email found:", employee.email)
    print("Stored hash:", employee.password_hash)
    print("Password entered:", password)
    print("Password valid:", employee.check_password(password))

    if not employee.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    if employee.status != "active":
        return jsonify({"error": "This account is inactive"}), 403

    access_token = create_access_token(identity=employee.employee_id)

    return jsonify({
        "token": access_token,
        "employee_id": employee.employee_id,
        "full_name": employee.full_name,
        "role_id": employee.role_id,
    }), 200


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    employee = Employee.query.filter_by(email=email).first()

    # Always return success even if email not found - avoids leaking which emails exist
    if not employee:
        return jsonify({"message": "If that email exists, a reset link has been sent."}), 200

    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(minutes=30)

    reset_entry = PasswordReset(
        employee_id=employee.employee_id,
        token=token,
        expires_at=expires_at,
    )
    db.session.add(reset_entry)
    db.session.commit()

    reset_link = f"{current_app.config['FRONTEND_URL']}/reset-password?token={token}"
    send_reset_email(employee.email, reset_link)

    return jsonify({"message": "If that email exists, a reset link has been sent."}), 200


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    token = data.get("token")
    new_password = data.get("new_password")

    if not token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400

    reset_entry = PasswordReset.query.filter_by(token=token, is_used=False).first()

    if not reset_entry:
        return jsonify({"error": "Invalid or already-used reset link"}), 400

    if reset_entry.expires_at < datetime.utcnow():
        return jsonify({"error": "Reset link has expired"}), 400

    employee = Employee.query.get(reset_entry.employee_id)
    employee.password_hash = generate_password_hash(new_password)

    reset_entry.is_used = True

    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200