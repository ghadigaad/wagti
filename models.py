from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(80), unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_guest   = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    activities = db.relationship("Activity", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Activity(db.Model):
    __tablename__ = "activities"

    id                = db.Column(db.Integer, primary_key=True)
    user_id           = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    task_name         = db.Column(db.String(200), nullable=False)
    category          = db.Column(db.String(50), nullable=False, default="Study")
    expected_duration = db.Column(db.Integer, default=25)  # minutes
    start_time        = db.Column(db.DateTime, nullable=True)
    end_time          = db.Column(db.DateTime, nullable=True)
    duration          = db.Column(db.Integer, default=0)   # seconds
    status            = db.Column(db.String(20), default="pending")  # pending/active/completed
    created_at        = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id":                self.id,
            "task_name":         self.task_name,
            "category":          self.category,
            "expected_duration": self.expected_duration,
            "start_time":        self.start_time.isoformat() if self.start_time else None,
            "end_time":          self.end_time.isoformat() if self.end_time else None,
            "duration":          self.duration,
            "status":            self.status,
            "created_at":        self.created_at.isoformat() if self.created_at else None,
        }
