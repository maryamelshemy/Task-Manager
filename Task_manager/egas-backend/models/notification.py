from datetime import datetime

from extensions import db


class Notification(db.Model):
    __tablename__ = "Notification"

    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("Employee.employee_id"), nullable=False)
    related_task_id = db.Column(db.Integer, db.ForeignKey("Task.task_id"))
    message = db.Column(db.String(255), nullable=False)
    type = db.Column(
        db.Enum("Deadline", "Assignment", "Attendance", "System", name="notification_type", native_enum=False),
        nullable=False,
    )
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employee = db.relationship("Employee", backref="notifications")
