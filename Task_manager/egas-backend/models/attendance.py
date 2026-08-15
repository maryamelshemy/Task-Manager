from datetime import date

from extensions import db


class Attendance(db.Model):
    __tablename__ = "Attendance"

    attendance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("Employee.employee_id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    check_in_time = db.Column(db.Time)
    check_out_time = db.Column(db.Time)
    status = db.Column(
        db.Enum("Present", "Absent", "Late", "On Leave", name="attendance_status", native_enum=False),
        default="Present",
    )

    __table_args__ = (
        db.UniqueConstraint("employee_id", "date"),
    )

    employee = db.relationship("Employee", back_populates="attendance_records")
