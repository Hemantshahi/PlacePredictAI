"""
routes/admin_routes.py — Admin Dashboard Routes
"""
import json
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user
from functools import wraps

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    from models.models import User, Prediction, ATSScore
    users = User.query.filter_by(role='student').order_by(User.created_at.desc()).all()
    total_users = len(users)
    total_predictions = Prediction.query.count()
    avg_prob = 0
    preds = Prediction.query.all()
    if preds:
        avg_prob = round(sum(p.placement_probability or 0 for p in preds) / len(preds), 1)
    placed_count = Prediction.query.filter(Prediction.placement_probability >= 75).count()

    return render_template('admin/dashboard.html',
                           users=users,
                           total_users=total_users,
                           total_predictions=total_predictions,
                           avg_prob=avg_prob,
                           placed_count=placed_count)


@admin_bp.route('/user/<int:user_id>')
@login_required
@admin_required
def user_detail(user_id):
    from models.models import User, Resume, Prediction, ATSScore, SkillGap
    user = User.query.get_or_404(user_id)
    resume = Resume.query.filter_by(user_id=user_id).first()
    predictions = Prediction.query.filter_by(user_id=user_id).order_by(
        Prediction.predicted_at.desc()).all()
    ats_scores = ATSScore.query.filter_by(user_id=user_id).order_by(
        ATSScore.scored_at.desc()).all()
    return render_template('admin/user_detail.html',
                           user=user,
                           student=user,
                           resume=resume,
                           predictions=predictions,
                           ats_scores=ats_scores,
                           skill_gaps=[])


@admin_bp.route('/user/<int:user_id>/ban', methods=['POST'])
@login_required
@admin_required
def ban_user(user_id):
    from models.models import User, db
    from app import db
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Admin account cannot be banned!', 'danger')
        return redirect(url_for('admin.dashboard'))
    user.is_active_user = not user.is_active_user
    db.session.commit()
    status = 'banned' if not user.is_active_user else 'unbanned'
    flash(f'{user.name} ko {status} kar diya gaya! ✅', 'success')
    return redirect(url_for('admin.user_detail', user_id=user_id))


@admin_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_profile():
    from app import db, bcrypt
    if request.method == 'POST':
        current_user.name = request.form.get('name', current_user.name).strip()
        current_user.phone = request.form.get('phone', '').strip()
        new_password = request.form.get('new_password', '').strip()
        if new_password:
            current_user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        flash('Profile updated! ✅', 'success')
        return redirect(url_for('admin.admin_profile'))
    return render_template('admin/profile.html')


@admin_bp.route('/analytics-data')
@login_required
@admin_required
def analytics_data():
    from models.models import Prediction, ATSScore, User
    placed = Prediction.query.filter(Prediction.placement_probability >= 75).count()
    average = Prediction.query.filter(
        Prediction.placement_probability >= 50,
        Prediction.placement_probability < 75).count()
    needs_work = Prediction.query.filter(Prediction.placement_probability < 50).count()

    ats_all = ATSScore.query.all()
    ats_buckets = {'0-25': 0, '26-50': 0, '51-75': 0, '76-100': 0}
    for a in ats_all:
        s = a.total_score or 0
        if s <= 25: ats_buckets['0-25'] += 1
        elif s <= 50: ats_buckets['26-50'] += 1
        elif s <= 75: ats_buckets['51-75'] += 1
        else: ats_buckets['76-100'] += 1

    users = User.query.filter_by(role='student').all()
    branch_counts = {}
    for u in users:
        b = u.branch or 'Unknown'
        branch_counts[b] = branch_counts.get(b, 0) + 1

    return jsonify({
        'placement_distribution': {'placed': placed, 'average': average, 'needs_work': needs_work},
        'ats_distribution': ats_buckets,
        'branch_distribution': branch_counts,
    })
@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    from models.models import User, Resume, Prediction, ATSScore, SkillGap, ChatHistory, CompanyRecommendation, db
    from app import db

    user = User.query.get_or_404(user_id)

    if user.role == 'admin':
        flash('Admin account cannot be deleted!', 'danger')
        return redirect(url_for('admin.dashboard'))

    # Sab related data delete karo
    ChatHistory.query.filter_by(user_id=user_id).delete()
    ATSScore.query.filter_by(user_id=user_id).delete()
    Prediction.query.filter_by(user_id=user_id).delete()
    SkillGap.query.filter_by(user_id=user_id).delete()
    CompanyRecommendation.query.filter_by(user_id=user_id).delete()
    Resume.query.filter_by(user_id=user_id).delete()
    db.session.delete(user)
    db.session.commit()

    flash(f'Student "{user.name}" has been removed successfully!', 'success')
    return redirect(url_for('admin.dashboard'))