from datetime import date

from extensions import db


class EmployeeCategory(db.Model):
    __tablename__ = "Employee_Category"

    employee_category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("Employee.employee_id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("Category.category_id"), nullable=False)
    assigned_date = db.Column(db.Date, default=date.today)

    __table_args__ = (
        db.UniqueConstraint("employee_id", "category_id"),
    )

    employee = db.relationship("Employee", backref="category_links")
