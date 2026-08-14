from extensions import db


class Category(db.Model):
    __tablename__ = "Category"

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey("Employee.employee_id"))

    creator = db.relationship("Employee", foreign_keys=[created_by], backref="created_categories")
    tasks = db.relationship("Task", backref="category", lazy=True)
    employee_links = db.relationship("EmployeeCategory", backref="category", lazy=True)
