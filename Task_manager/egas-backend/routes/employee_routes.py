from flask import Blueprint, jsonify, request

from utils.decorators import login_required, manager_required
from extensions import db
from models.attendance import Attendance
from models.category import Category
from models.comment import Comment
from models.employee import Employee
from models.employee_category import EmployeeCategory
from models.notification import Notification
from models.reminder import Reminder
from models.report_history import ReportHistory
from models.role import Role
from models.task import Task
from models.task_history import TaskHistory

employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/employees", methods=["GET"])
@login_required
def get_employees():
    employees = Employee.query.order_by(Employee.employee_id).all()
    return jsonify([employee.to_dict() for employee in employees]), 200


@employee_bp.route("/employees/<int:employee_id>", methods=["GET"])
@login_required
def get_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return jsonify(employee.to_dict()), 200


@employee_bp.route("/employees", methods=["POST"])
@manager_required
def create_employee():
    data = request.get_json(silent=True) or {}

    required_fields = ["full_name", "email", "password_hash", "role_id"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    if Employee.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Employee with this email already exists"}), 409

    employee = Employee(
        full_name=data["full_name"],
        email=data["email"],
        password_hash=data["password_hash"],
        phone_number=data.get("phone_number"),
        hire_date=data.get("hire_date"),
        role_id=data["role_id"],
        profile_photo=data.get("profile_photo"),
        status=data.get("status", "active"),
    )
    db.session.add(employee)
    db.session.commit()

    return jsonify(employee.to_dict()), 201


@employee_bp.route("/employees/<int:employee_id>", methods=["PUT"])
@manager_required
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    data = request.get_json(silent=True) or {}

    for field in ["full_name", "email", "phone_number", "hire_date", "role_id", "profile_photo", "status"]:
        if field in data:
            setattr(employee, field, data[field])

    if "password_hash" in data and data["password_hash"]:
        employee.password_hash = data["password_hash"]

    db.session.commit()
    return jsonify(employee.to_dict()), 200


@employee_bp.route("/employees/<int:employee_id>", methods=["DELETE"])
@manager_required
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({"message": "Employee deleted successfully"}), 200


@employee_bp.route("/roles", methods=["GET"])
@login_required
def get_roles():
    roles = Role.query.order_by(Role.role_id).all()
    return jsonify([{"role_id": role.role_id, "role_name": role.role_name} for role in roles]), 200


@employee_bp.route("/categories", methods=["GET"])
@login_required
def get_categories():
    categories = Category.query.order_by(Category.category_id).all()
    return jsonify([
        {
            "category_id": category.category_id,
            "category_name": category.category_name,
            "description": category.description,
            "created_by": category.created_by,
        }
        for category in categories
    ]), 200


@employee_bp.route("/categories", methods=["POST"])
@manager_required
def create_category():
    data = request.get_json(silent=True) or {}
    category_name = data.get("category_name")
    if not category_name:
        return jsonify({"error": "category_name is required"}), 400

    if Category.query.filter_by(category_name=category_name).first():
        return jsonify({"error": "Category already exists"}), 409

    category = Category(
        category_name=category_name,
        description=data.get("description"),
        created_by=data.get("created_by"),
    )
    db.session.add(category)
    db.session.commit()
    return jsonify({
        "category_id": category.category_id,
        "category_name": category.category_name,
        "description": category.description,
        "created_by": category.created_by,
    }), 201


@employee_bp.route("/employee-categories", methods=["GET"])
@login_required
def get_employee_categories():
    items = EmployeeCategory.query.order_by(EmployeeCategory.employee_category_id).all()
    return jsonify([
        {
            "employee_category_id": item.employee_category_id,
            "employee_id": item.employee_id,
            "category_id": item.category_id,
            "assigned_date": item.assigned_date.isoformat() if item.assigned_date else None,
        }
        for item in items
    ]), 200


@employee_bp.route("/employee-categories", methods=["POST"])
@manager_required
def create_employee_category():
    data = request.get_json(silent=True) or {}
    employee_id = data.get("employee_id")
    category_id = data.get("category_id")

    if not employee_id or not category_id:
        return jsonify({"error": "employee_id and category_id are required"}), 400

    if EmployeeCategory.query.filter_by(employee_id=employee_id, category_id=category_id).first():
        return jsonify({"error": "This employee is already assigned to this category"}), 409

    item = EmployeeCategory(employee_id=employee_id, category_id=category_id)
    db.session.add(item)
    db.session.commit()
    return jsonify({
        "employee_category_id": item.employee_category_id,
        "employee_id": item.employee_id,
        "category_id": item.category_id,
        "assigned_date": item.assigned_date.isoformat() if item.assigned_date else None,
    }), 201


@employee_bp.route("/tasks", methods=["GET"])
@login_required
def get_tasks():
    tasks = Task.query.order_by(Task.task_id).all()
    return jsonify([
        {
            "task_id": task.task_id,
            "title": task.title,
            "description": task.description,
            "category_id": task.category_id,
            "assigned_to": task.assigned_to,
            "assigned_by": task.assigned_by,
            "created_date": task.created_date.isoformat() if task.created_date else None,
            "deadline": task.deadline.isoformat() if task.deadline else None,
            "priority": task.priority,
            "status": task.status,
            "completed_date": task.completed_date.isoformat() if task.completed_date else None,
        }
        for task in tasks
    ]), 200


@employee_bp.route("/tasks", methods=["POST"])
@login_required
def create_task():
    data = request.get_json(silent=True) or {}
    required_fields = ["title", "category_id", "assigned_to", "assigned_by"]
    missing = [field for field in required_fields if data.get(field) in (None, "")]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    task = Task(
        title=data["title"],
        description=data.get("description"),
        category_id=data["category_id"],
        assigned_to=data["assigned_to"],
        assigned_by=data["assigned_by"],
        deadline=data.get("deadline"),
        priority=data.get("priority", "Medium"),
        status=data.get("status", "Not Started"),
        completed_date=data.get("completed_date"),
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({
        "task_id": task.task_id,
        "title": task.title,
        "description": task.description,
        "category_id": task.category_id,
        "assigned_to": task.assigned_to,
        "assigned_by": task.assigned_by,
        "priority": task.priority,
        "status": task.status,
    }), 201


@employee_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json(silent=True) or {}

    for field in ["title", "description", "category_id", "assigned_to", "assigned_by", "deadline", "priority", "status", "completed_date"]:
        if field in data:
            setattr(task, field, data[field])

    db.session.commit()
    return jsonify({
        "task_id": task.task_id,
        "title": task.title,
        "description": task.description,
        "category_id": task.category_id,
        "assigned_to": task.assigned_to,
        "assigned_by": task.assigned_by,
        "deadline": task.deadline.isoformat() if task.deadline else None,
        "priority": task.priority,
        "status": task.status,
        "completed_date": task.completed_date.isoformat() if task.completed_date else None,
    }), 200


@employee_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@manager_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"}), 200


@employee_bp.route("/task-history", methods=["GET"])
@login_required
def get_task_history():
    records = TaskHistory.query.order_by(TaskHistory.history_id).all()
    return jsonify([
        {
            "history_id": record.history_id,
            "task_id": record.task_id,
            "changed_by": record.changed_by,
            "old_status": record.old_status,
            "new_status": record.new_status,
            "changed_at": record.changed_at.isoformat() if record.changed_at else None,
        }
        for record in records
    ]), 200


@employee_bp.route("/task-history", methods=["POST"])
@login_required
def create_task_history():
    data = request.get_json(silent=True) or {}
    if not data.get("task_id") or not data.get("changed_by"):
        return jsonify({"error": "task_id and changed_by are required"}), 400

    record = TaskHistory(
        task_id=data["task_id"],
        changed_by=data["changed_by"],
        old_status=data.get("old_status"),
        new_status=data.get("new_status"),
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({
        "history_id": record.history_id,
        "task_id": record.task_id,
        "changed_by": record.changed_by,
        "old_status": record.old_status,
        "new_status": record.new_status,
        "changed_at": record.changed_at.isoformat() if record.changed_at else None,
    }), 201


@employee_bp.route("/attendance", methods=["GET"])
@login_required
def get_attendance():
    records = Attendance.query.order_by(Attendance.attendance_id).all()
    return jsonify([
        {
            "attendance_id": record.attendance_id,
            "employee_id": record.employee_id,
            "date": record.date.isoformat() if record.date else None,
            "check_in_time": record.check_in_time.isoformat() if record.check_in_time else None,
            "check_out_time": record.check_out_time.isoformat() if record.check_out_time else None,
            "status": record.status,
        }
        for record in records
    ]), 200


@employee_bp.route("/attendance", methods=["POST"])
@manager_required
def create_attendance():
    data = request.get_json(silent=True) or {}
    if not data.get("employee_id") or not data.get("date"):
        return jsonify({"error": "employee_id and date are required"}), 400

    record = Attendance(
        employee_id=data["employee_id"],
        date=data["date"],
        check_in_time=data.get("check_in_time"),
        check_out_time=data.get("check_out_time"),
        status=data.get("status", "Present"),
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({
        "attendance_id": record.attendance_id,
        "employee_id": record.employee_id,
        "date": record.date.isoformat() if record.date else None,
        "check_in_time": record.check_in_time.isoformat() if record.check_in_time else None,
        "check_out_time": record.check_out_time.isoformat() if record.check_out_time else None,
        "status": record.status,
    }), 201


@employee_bp.route("/reminders", methods=["GET"])
@login_required
def get_reminders():
    reminders = Reminder.query.order_by(Reminder.reminder_id).all()
    return jsonify([
        {
            "reminder_id": reminder.reminder_id,
            "task_id": reminder.task_id,
            "employee_id": reminder.employee_id,
            "remind_at": reminder.remind_at.isoformat() if reminder.remind_at else None,
            "message": reminder.message,
            "is_sent": reminder.is_sent,
        }
        for reminder in reminders
    ]), 200


@employee_bp.route("/notifications", methods=["GET"])
@login_required
def get_notifications():
    notifications = Notification.query.order_by(Notification.notification_id).all()
    return jsonify([
        {
            "notification_id": notification.notification_id,
            "employee_id": notification.employee_id,
            "related_task_id": notification.related_task_id,
            "message": notification.message,
            "type": notification.type,
            "is_read": notification.is_read,
            "created_at": notification.created_at.isoformat() if notification.created_at else None,
        }
        for notification in notifications
    ]), 200


@employee_bp.route("/comments", methods=["GET"])
@login_required
def get_comments():
    comments = Comment.query.order_by(Comment.comment_id).all()
    return jsonify([
        {
            "comment_id": comment.comment_id,
            "task_id": comment.task_id,
            "employee_id": comment.employee_id,
            "comment_text": comment.comment_text,
            "created_at": comment.created_at.isoformat() if comment.created_at else None,
        }
        for comment in comments
    ]), 200


@employee_bp.route("/reports", methods=["GET"])
@login_required
def get_reports():
    reports = ReportHistory.query.order_by(ReportHistory.report_id).all()
    return jsonify([
        {
            "report_id": report.report_id,
            "employee_id": report.employee_id,
            "report_type": report.report_type,
            "generated_at": report.generated_at.isoformat() if report.generated_at else None,
            "report_data": report.report_data,
        }
        for report in reports
    ]), 200


@employee_bp.route("/reports", methods=["POST"])
@manager_required
def create_report():
    data = request.get_json(silent=True) or {}
    if not data.get("employee_id") or not data.get("report_type"):
        return jsonify({"error": "employee_id and report_type are required"}), 400

    report = ReportHistory(
        employee_id=data["employee_id"],
        report_type=data["report_type"],
        report_data=data.get("report_data"),
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({
        "report_id": report.report_id,
        "employee_id": report.employee_id,
        "report_type": report.report_type,
        "generated_at": report.generated_at.isoformat() if report.generated_at else None,
        "report_data": report.report_data,
    }), 201