"""
routes/resume_routes.py — Resume Upload & Manual Input Routes
"""
import os
import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

resume_bp = Blueprint('resume', __name__)

ALLOWED = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED


@resume_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    from app import db
    from models.models import Resume
    from utils.resume_parser import resume_parser
    from utils.ats_scorer import ats_scorer

    if request.method == 'POST':
        mode = request.form.get('mode', 'upload')

        if mode == 'upload' and 'resume_file' in request.files:
            file = request.files['resume_file']
            if file and allowed_file(file.filename):

                # Purane resumes inactive karo
                Resume.query.filter_by(
                    user_id=current_user.id
                ).update({'is_active': False})

                # Naya resume banao
                resume = Resume(
                    user_id=current_user.id,
                    is_active=True,
                    resume_name=file.filename,
                    uploaded_at=datetime.utcnow()
                )
                db.session.add(resume)

                filename = secure_filename(
                    f"user_{current_user.id}_{file.filename}"
                )
                filepath = os.path.join(
                    current_app.config['UPLOAD_FOLDER'], filename
                )
                file.save(filepath)
                resume.file_path = filepath

                # Parse resume
                text   = resume_parser.extract_text(filepath)
                parsed = resume_parser.parse(text)

                resume.extracted_skills    = json.dumps(parsed.get('skills', []))
                resume.extracted_name      = parsed.get('name')
                resume.extracted_email     = parsed.get('email')
                resume.extracted_phone     = parsed.get('phone')
                resume.extracted_education = json.dumps(parsed.get('education', []))
                resume.extracted_projects  = json.dumps(parsed.get('projects', []))

                if parsed.get('cgpa'):
                    resume.cgpa = parsed['cgpa']
                if parsed.get('internship_count'):
                    resume.internship_count = parsed['internship_count']
                if parsed.get('project_count'):
                    resume.project_count = parsed['project_count']
                if parsed.get('certification_count'):
                    resume.certifications_count = parsed['certification_count']

                # ATS Score
                job_role = request.form.get('target_role', 'Software Engineer')
                resume.target_role = job_role
                ats_result = ats_scorer.score(text, job_role)

                from models.models import ATSScore
                ats_entry = ATSScore(
                    user_id=current_user.id,
                    total_score=ats_result['total_score'],
                    keyword_score=ats_result['breakdown']['keyword_score'],
                    format_score=ats_result['breakdown']['format_score'],
                    completeness_score=ats_result['breakdown']['section_score'],
                    suggestions=json.dumps(ats_result['suggestions']),
                    job_role=job_role
                )
                db.session.add(ats_entry)
                db.session.commit()

                flash('Resume uploaded and analyzed successfully!', 'success')
                return redirect(url_for('resume.result'))

        elif mode == 'manual':
            # Purane resumes inactive karo
            Resume.query.filter_by(
                user_id=current_user.id
            ).update({'is_active': False})

            # Naya manual resume banao
            resume = Resume(
                user_id=current_user.id,
                is_active=True,
                resume_name='Manual Profile',
                uploaded_at=datetime.utcnow()
            )
            db.session.add(resume)

            resume.cgpa                  = float(request.form.get('cgpa', 0) or 0)
            resume.tenth_percent         = float(request.form.get('tenth_percent', 0) or 0)
            resume.twelfth_percent       = float(request.form.get('twelfth_percent', 0) or 0)
            resume.backlogs              = int(request.form.get('backlogs', 0) or 0)
            resume.internship_count      = int(request.form.get('internships', 0) or 0)
            resume.project_count         = int(request.form.get('projects', 0) or 0)
            resume.certifications_count  = int(request.form.get('certifications', 0) or 0)
            resume.communication_skill   = int(request.form.get('communication', 5) or 5)
            resume.coding_skill          = int(request.form.get('coding_skill', 5) or 5)
            resume.aptitude_score        = float(request.form.get('aptitude', 50) or 50)
            resume.technical_skill_score = float(request.form.get('technical', 50) or 50)
            resume.extracurricular       = int(request.form.get('extracurricular', 0) or 0)
            resume.target_role           = request.form.get('target_role', 'Software Engineer')

            skills_raw  = request.form.get('skills', '')
            skills_list = [s.strip().lower() for s in skills_raw.split(',') if s.strip()]
            resume.extracted_skills = json.dumps(skills_list)

            db.session.commit()
            flash('Profile saved successfully!', 'success')
            return redirect(url_for('predict.run'))

    return render_template('resume/upload.html')


@resume_bp.route('/result')
@login_required
def result():
    from models.models import Resume, ATSScore

    resume = Resume.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).order_by(Resume.uploaded_at.desc()).first()

    if not resume:
        resume = Resume.query.filter_by(
            user_id=current_user.id
        ).order_by(Resume.uploaded_at.desc()).first()

    ats = ATSScore.query.filter_by(
        user_id=current_user.id
    ).order_by(ATSScore.scored_at.desc()).first()

    ats_result = None
    if ats:
        ats_result = {
            'score':    ats.total_score or 0,
            'breakdown': {
                'keywords': ats.keyword_score or 0,
                'sections': ats.completeness_score or 0,
                'format':   ats.format_score or 0,
                'contact':  ats.experience_score or 0,
            },
            'suggestions':       ats.get_suggestions() if ats else [],
            'matched_keywords':  []
        }

    parsed_data = None
    if resume:
        parsed_data = {
            'name':   resume.extracted_name,
            'email':  resume.extracted_email,
            'phone':  resume.extracted_phone,
            'cgpa':   resume.cgpa,
            'skills': resume.get_skills(),
        }

    return render_template('resume/result.html',
                           resume=resume,
                           ats=ats,
                           ats_result=ats_result,
                           parsed_data=parsed_data)


@resume_bp.route('/set-active/<int:resume_id>', methods=['POST'])
@login_required
def set_active(resume_id):
    from app import db
    from models.models import Resume

    # Pehle sab inactive karo
    Resume.query.filter_by(
        user_id=current_user.id
    ).update({'is_active': False})

    # Selected resume active karo
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id:
        flash('Access denied!', 'danger')
        return redirect(url_for('main.profile'))

    resume.is_active = True
    db.session.commit()

    flash('Resume switched! Running new prediction...', 'success')
    return redirect(url_for('predict.run'))

@resume_bp.route('/delete/<int:resume_id>', methods=['POST'])
@login_required
def delete_resume(resume_id):
    from app import db
    from models.models import Resume, Prediction, SkillGap, CompanyRecommendation, ATSScore

    resume = Resume.query.get_or_404(resume_id)

    if resume.user_id != current_user.id:
        flash('Access denied!', 'danger')
        return redirect(url_for('main.profile'))

    was_active = resume.is_active

    # Related data delete karo
    ATSScore.query.filter_by(user_id=current_user.id).delete()
    Prediction.query.filter_by(user_id=current_user.id).delete()
    SkillGap.query.filter_by(user_id=current_user.id).delete()
    CompanyRecommendation.query.filter_by(user_id=current_user.id).delete()

    db.session.delete(resume)
    db.session.commit()

    # Agar active tha toh doosra active karo
    if was_active:
        latest = Resume.query.filter_by(
            user_id=current_user.id
        ).order_by(Resume.uploaded_at.desc()).first()
        if latest:
            latest.is_active = True
            db.session.commit()

    flash('Resume deleted successfully!', 'success')
    return redirect(url_for('main.profile'))