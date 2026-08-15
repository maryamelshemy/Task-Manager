from extensions import db


class Category(db.Model):
    __tablename__ = "Category"

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey("Employee.employee_id"))

    employee = db.relationship("Employee", back_populates="report_history")
    tasks = db.relationship("Task", backref="category", lazy=True)
    employee_links = db.relationship("EmployeeCategory", backref="category", lazy=True)
