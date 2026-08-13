from extensions import db
from werkzeug.security import check_password_hash, generate_password_hash

class Employee(db.Model):
    __tablename__ = "Employee"

    employee_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20))
    hire_date = db.Column(db.Date)
    role_id = db.Column(db.Integer, db.ForeignKey("Role.role_id"), nullable=False)
    profile_photo = db.Column(db.String(255))
    status = db.Column(db.Enum("active", "inactive"), default="active")

    def check_password(self, plain_password):
        return check_password_hash(self.password_hash, plain_password)

    def set_password(self, plain_password):
        self.password_hash = generate_password_hash(plain_password)