from datetime import datetime

from extensions import db


class Comment(db.Model):
    __tablename__ = "Comment"

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey("Task.task_id"), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("Employee.employee_id"), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

   employee = db.relationship("Employee", back_populates="comments")
