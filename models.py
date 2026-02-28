from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    
    """User model for students, teachers, and admins"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student, teacher, admin
    sub_role = db.Column(db.String(20), nullable=True)  # superadmin / branchadmin
    name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(50))  # CSE-AI&DS, Civil, Electrical
    semester = db.Column(db.Integer, default=1)
    imported_file_id = db.Column(db.Integer, db.ForeignKey('uploaded_file.id'))
    academic_year = db.Column(db.String(20))
    roll_number = db.Column(db.String(20))
    subject = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    feedbacks_given = db.relationship('Feedback', 
                                      foreign_keys='Feedback.student_id',
                                      backref='student', 
                                      lazy='dynamic')
    
    feedbacks_received = db.relationship('Feedback', 
                                         foreign_keys='Feedback.teacher_id',
                                         backref='teacher', 
                                         lazy='dynamic')
    
    def get_id(self):
        return self.id
        
# models.py
class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)  # student / teacher / admin
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Feedback(db.Model):
    """Feedback model for student feedback to teachers"""
    __tablename__ = 'feedbacks'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 rating
    comment = db.Column(db.Text)
    semester = db.Column(db.Integer, nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class PasswordReset(db.Model):
    """Password reset tokens"""
    __tablename__ = 'password_resets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reset_code = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)

