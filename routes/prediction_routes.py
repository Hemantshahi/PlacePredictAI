"""
routes/prediction_routes.py — Placement Prediction Routes
"""
import json
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

prediction_bp = Blueprint('predict', __name__)


@prediction_bp.route('/run')
@login_required
def run():
    from app import db
    from models.models import Resume, Prediction, SkillGap, CompanyRecommendation
    from utils.predictor import predictor, get_model_metrics
    from utils.skill_gap import skill_gap_analyzer, recommend_companies

    # Active resume lo
    resume = Resume.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).order_by(Resume.uploaded_at.desc()).first()

    # Agar active nahi mila toh latest lo
    if not resume:
        resume = Resume.query.filter_by(
            user_id=current_user.id
        ).order_by(Resume.uploaded_at.desc()).first()
    if not resume:
        flash('Please upload your resume or complete your profile first.', 'warning')
        return redirect(url_for('resume.upload'))

    # Build feature dict
    features = {
        'cgpa':             resume.cgpa or 7.0,
        'tenth_percent':    resume.tenth_percent or 0.0,
        'twelfth_percent':  resume.twelfth_percent or 0.0,
        'backlogs':              resume.backlogs or 0,
        'internships':           resume.internship_count or 0,
        'projects':              resume.project_count or 0,
        'certifications':        resume.certifications_count or 0,
        'communication_skill':   resume.communication_skill or 5,
        'coding_skill':          resume.coding_skill or 5,
        'aptitude_score':        resume.aptitude_score or 50.0,
        'technical_skill_score': resume.technical_skill_score or 50.0,
        'extracurricular':       resume.extracurricular or 0,
        'ats_score':             60.0,
    }

    # Get ATS score
    from models.models import ATSScore
    ats = ATSScore.query.filter_by(user_id=current_user.id).order_by(
        ATSScore.scored_at.desc()).first()
    if ats:
        features['ats_score'] = ats.total_score

    # Run prediction
    pred_result = predictor.predict(features)

    # Save prediction to DB
    pred_entry = Prediction(
        user_id=current_user.id,
        rf_score=pred_result['rf_score'],
        xgb_score=pred_result['xgb_score'],
        ann_score=pred_result['ann_score'],
        ensemble_score=pred_result['ensemble_score'],
        placement_probability=pred_result['placement_probability'],
        placement_status=pred_result['placement_status'],
        confidence=pred_result['confidence'],
        input_features=json.dumps(features)
    )
    db.session.add(pred_entry)

    # Skill Gap Analysis
    user_skills = resume.get_skills()
    job_role    = resume.target_role or 'Software Engineer'
    gap_result  = skill_gap_analyzer.analyze(user_skills, job_role)

    gap_entry = SkillGap(
        user_id=current_user.id,
        job_role=job_role,
        present_skills=json.dumps(gap_result['present_skills']),
        missing_skills=json.dumps(gap_result['missing_skills']),
        recommendations=json.dumps(gap_result['recommendations'])
    )
    db.session.add(gap_entry)

    # Company Recommendations
    companies = recommend_companies(
        user_skills,
        features['cgpa'],
        pred_result['placement_probability'],
        user_branch=current_user.branch
    )
    print(f"DEBUG — Branch: {current_user.branch}, Skills: {user_skills}, Companies: {len(companies)}")

    comp_entry = CompanyRecommendation(
        user_id=current_user.id,
        companies=json.dumps(companies)
    )
    db.session.add(comp_entry)
    db.session.commit()

    return render_template('prediction/result.html',
                           prediction=pred_result,
                           gap=gap_result,
                           companies=companies[:8],
                           features=features,
                           resume=resume)