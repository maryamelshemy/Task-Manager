from datetime import datetime

from extensions import db


class Reminder(db.Model):
    __tablename__ = "Reminder"

    reminder_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey("Task.task_id"), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("Employee.employee_id"), nullable=False)
    remind_at = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.String(255))
    is_sent = db.Column(db.Boolean, default=False)

   employee = db.relationship("Employee", back_populates="reminders")
