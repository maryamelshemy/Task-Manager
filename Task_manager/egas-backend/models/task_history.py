from datetime import datetime

from extensions import db


class TaskHistory(db.Model):
    __tablename__ = "Task_History"

    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey("Task.task_id"), nullable=False)
    changed_by = db.Column(db.Integer, db.ForeignKey("Employee.employee_id"), nullable=False)
    old_status = db.Column(db.String(50))
    new_status = db.Column(db.String(50))
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)

    changer = db.relationship("Employee", foreign_keys=[changed_by], backref="task_history_changes")
