from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='student')
    branch = db.Column(db.String(100))
    batch = db.Column(db.String(20))
    phone = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active_user = db.Column(db.Boolean, default=True)
    designation = db.Column(db.String(100))
    resume = db.relationship('Resume', backref='user', uselist=False, lazy=True)
    predictions = db.relationship('Prediction', backref='user', lazy=True)
    ats_scores = db.relationship('ATSScore', backref='user', lazy=True)
    department  = db.Column(db.String(100))
    employee_id = db.Column(db.String(50))

class Resume(db.Model):
    __tablename__ = 'resumes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_path = db.Column(db.String(300))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    cgpa = db.Column(db.Float)
    tenth_percent = db.Column(db.Float)
    twelfth_percent = db.Column(db.Float)
    backlogs = db.Column(db.Integer, default=0)
    internship_count = db.Column(db.Integer, default=0)
    project_count = db.Column(db.Integer, default=0)
    certifications_count = db.Column(db.Integer, default=0)
    extracurricular = db.Column(db.Integer, default=0)
    communication_skill = db.Column(db.Integer, default=5)
    technical_skill_score = db.Column(db.Float)
    aptitude_score = db.Column(db.Float)
    coding_skill = db.Column(db.Integer, default=5)
    extracted_skills = db.Column(db.Text)
    extracted_name = db.Column(db.String(120))
    extracted_email = db.Column(db.String(150))
    extracted_phone = db.Column(db.String(20))
    extracted_education = db.Column(db.Text)
    extracted_experience = db.Column(db.Text)
    extracted_projects = db.Column(db.Text)
    target_role  = db.Column(db.String(100))
    is_active    = db.Column(db.Boolean, default=True)
    resume_name  = db.Column(db.String(200))
    uploaded_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def get_skills(self):
        return json.loads(self.extracted_skills) if self.extracted_skills else []

class ATSScore(db.Model):
    __tablename__ = 'ats_scores'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_score = db.Column(db.Float)
    keyword_score = db.Column(db.Float)
    format_score = db.Column(db.Float)
    completeness_score = db.Column(db.Float)
    experience_score = db.Column(db.Float)
    education_score = db.Column(db.Float)
    suggestions = db.Column(db.Text)
    job_role = db.Column(db.String(100))
    scored_at = db.Column(db.DateTime, default=datetime.utcnow)
    def get_suggestions(self):
        return json.loads(self.suggestions) if self.suggestions else []

class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rf_score = db.Column(db.Float)
    xgb_score = db.Column(db.Float)
    ann_score = db.Column(db.Float)
    ensemble_score = db.Column(db.Float)
    placement_probability = db.Column(db.Float)
    placement_status = db.Column(db.String(20))
    confidence = db.Column(db.String(20))
    predicted_at = db.Column(db.DateTime, default=datetime.utcnow)
    input_features = db.Column(db.Text)

class SkillGap(db.Model):
    __tablename__ = 'skill_gaps'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_role = db.Column(db.String(100))
    present_skills = db.Column(db.Text)
    missing_skills = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)
    def get_missing(self):
        return json.loads(self.missing_skills) if self.missing_skills else []

class CompanyRecommendation(db.Model):
    __tablename__ = 'company_recommendations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    companies = db.Column(db.Text)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatHistory(db.Model):
    __tablename__ = 'chat_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(20))
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)