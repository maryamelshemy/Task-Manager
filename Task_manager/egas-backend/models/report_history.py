from datetime import datetime

from extensions import db


class ReportHistory(db.Model):
    __tablename__ = "Report_History"

    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("Employee.employee_id"), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    report_data = db.Column(db.Text)

    employee = db.relationship("Employee", backref="report_history")
