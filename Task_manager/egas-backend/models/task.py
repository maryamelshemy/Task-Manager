from datetime import datetime

from extensions import db


class Task(db.Model):
    __tablename__ = "Task"

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey("Category.category_id"), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey("Employee.employee_id"), nullable=False)
    assigned_by = db.Column(db.Integer, db.ForeignKey("Employee.employee_id"), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    priority = db.Column(
        db.Enum("Low", "Medium", "High", "Urgent", name="task_priority", native_enum=False),
        default="Medium",
    )
    status = db.Column(
        db.Enum("Not Started", "In Progress", "Completed", "Overdue", "Cancelled", name="task_status", native_enum=False),
        default="Not Started",
    )
    completed_date = db.Column(db.DateTime, nullable=True)

    assignee = db.relationship("Employee", foreign_keys=[assigned_to], back_populates="assigned_tasks")
    assigner = db.relationship("Employee", foreign_keys=[assigned_by], back_populates="created_tasks")
    history = db.relationship("TaskHistory", backref="task", lazy=True)
    reminders = db.relationship("Reminder", backref="task", lazy=True)
    notifications = db.relationship("Notification", backref="task", lazy=True)
    comments = db.relationship("Comment", backref="task", lazy=True)
