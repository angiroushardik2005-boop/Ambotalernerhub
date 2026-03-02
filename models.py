from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# This will be initialized in app.py
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for students"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    roll_number = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_photo = db.Column(db.String(255), default='default.png')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to uploads
    uploads = db.relationship('Upload', backref='uploader', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Upload(db.Model):
    """Upload model for study materials"""
    __tablename__ = 'uploads'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(100), default='Study Material')  # Study Material, Question Papers (Sem X), Notes, etc.
    file_path = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(255))  # Optional cover image
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploader_name = db.Column(db.String(100), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Upload {self.title}>'
