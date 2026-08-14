from extensions import db
from werkzeug.security import check_password_hash, generate_password_hash


class Employee(db.Model):
    __tablename__ = "Employee"

    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20))
    hire_date = db.Column(db.Date)
    role_id = db.Column(db.Integer, db.ForeignKey("Role.role_id"), nullable=False)
    profile_photo = db.Column(db.String(255))
    status = db.Column(db.Enum("active", "inactive"), default="active")

    role = db.relationship("Role", back_populates="employees")
    category_links = db.relationship("EmployeeCategory", back_populates="employee", cascade="all, delete-orphan")
    attendance_records = db.relationship("Attendance", back_populates="employee", cascade="all, delete-orphan")
    notifications = db.relationship("Notification", back_populates="employee", cascade="all, delete-orphan")
    reminders = db.relationship("Reminder", back_populates="employee", cascade="all, delete-orphan")
    comments = db.relationship("Comment", back_populates="employee", cascade="all, delete-orphan")
    report_history = db.relationship("ReportHistory", back_populates="employee", cascade="all, delete-orphan")
    created_categories = db.relationship("Category", back_populates="creator", foreign_keys="Category.created_by")
    assigned_tasks = db.relationship("Task", foreign_keys="Task.assigned_to", back_populates="assignee", cascade="all, delete-orphan")
    created_tasks = db.relationship("Task", foreign_keys="Task.assigned_by", back_populates="assigner", cascade="all, delete-orphan")
    task_history_changes = db.relationship("TaskHistory", foreign_keys="TaskHistory.changed_by", back_populates="changer", cascade="all, delete-orphan")

    def check_password(self, plain_password):
        return check_password_hash(self.password_hash, plain_password)

    def set_password(self, plain_password):
        self.password_hash = generate_password_hash(plain_password)

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "hire_date": self.hire_date.isoformat() if self.hire_date else None,
            "role_id": self.role_id,
            "profile_photo": self.profile_photo,
            "status": self.status,
        }