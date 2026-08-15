from extensions import db


class Role(db.Model):
    __tablename__ = "Role"

    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), nullable=False, unique=True)

    employees = db.relationship("Employee", back_populates="role", lazy=True)
