"""
routes/main_routes.py — Main Application Routes
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    from models.models import Resume, Prediction, ATSScore, SkillGap
    if current_user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    resume = Resume.query.filter_by(user_id=current_user.id).first()
    latest_pred = Prediction.query.filter_by(
        user_id=current_user.id).order_by(Prediction.predicted_at.desc()).first()
    latest_ats = ATSScore.query.filter_by(
        user_id=current_user.id).order_by(ATSScore.scored_at.desc()).first()
    latest_gap = SkillGap.query.filter_by(
        user_id=current_user.id).order_by(SkillGap.analyzed_at.desc()).first()
    return render_template('dashboard.html',
                           resume=resume,
                           prediction=latest_pred,
                           ats=latest_ats,
                           gap=latest_gap)


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    from models.models import Resume, db
    from app import db
    resume = Resume.query.filter_by(user_id=current_user.id).first()

    if request.method == 'POST':
        current_user.name  = request.form.get('name', current_user.name).strip()
        current_user.phone = request.form.get('phone', '').strip()

        if current_user.role == 'admin':
            current_user.designation = request.form.get('designation', '').strip()
            current_user.department  = request.form.get('department', '').strip()
            current_user.employee_id = request.form.get('employee_id', '').strip()
        else:
            current_user.branch = request.form.get('branch', current_user.branch)
            current_user.batch  = request.form.get('batch', current_user.batch)

        new_password     = request.form.get('new_password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if new_password:
            if new_password == confirm_password:
                from app import bcrypt
                current_user.password_hash = bcrypt.generate_password_hash(
                    new_password).decode('utf-8')
            else:
                flash('Passwords do not match. Please try again.', 'danger')
                return redirect(url_for('main.profile'))

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))

    from models.models import Resume as ResumeModel
    all_resumes = ResumeModel.query.filter_by(
        user_id=current_user.id
    ).order_by(ResumeModel.uploaded_at.desc()).all()

    return render_template('profile.html',
                           resume=resume,
                           resumes=all_resumes)