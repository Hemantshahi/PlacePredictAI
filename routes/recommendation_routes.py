from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.models import SkillGap
import json

recommend_bp = Blueprint('recommend', __name__, url_prefix='/recommendations')

# ─── Curated Resource Database ───────────────────────────────────────────────

SKILL_RESOURCES = {
    "python": {
        "youtube": [
            {"title": "Python for Beginners — freeCodeCamp", "url": "https://www.youtube.com/watch?v=rfscVS0vtbw", "duration": "4.5 hrs", "channel": "freeCodeCamp"},
            {"title": "Python Full Course — Corey Schafer", "url": "https://www.youtube.com/watch?v=YYXdXT2l-Gg", "duration": "9 hrs", "channel": "Corey Schafer"},
            {"title": "Python Advanced Concepts", "url": "https://www.youtube.com/watch?v=p15xzjzR9j0", "duration": "2 hrs", "channel": "Tech With Tim"},
        ],
        "roadmap": ["Variables & Data Types", "Functions & OOP", "File I/O", "Libraries (NumPy, Pandas)", "Projects"],
        "time": "4-6 weeks"
    },
    "sql": {
        "youtube": [
            {"title": "SQL Full Course — freeCodeCamp", "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY", "duration": "4.2 hrs", "channel": "freeCodeCamp"},
            {"title": "SQL Tutorial — Programming with Mosh", "url": "https://www.youtube.com/watch?v=7S_tz1z_5bA", "duration": "3 hrs", "channel": "Mosh"},
            {"title": "Advanced SQL for Data Analysis", "url": "https://www.youtube.com/watch?v=OT1RErkfLNQ", "duration": "2 hrs", "channel": "Alex The Analyst"},
        ],
        "roadmap": ["SELECT & Filters", "JOINs & Subqueries", "Aggregations", "Window Functions", "Stored Procedures"],
        "time": "3-4 weeks"
    },
    "machine learning": {
        "youtube": [
            {"title": "ML Course — Andrew Ng (Stanford)", "url": "https://www.youtube.com/watch?v=PPLop4L2eGk", "duration": "Full Course", "channel": "DeepLearning.AI"},
            {"title": "Machine Learning A-Z — Krish Naik", "url": "https://www.youtube.com/watch?v=GwIo3gDZCVQ", "duration": "10 hrs", "channel": "Krish Naik"},
            {"title": "Scikit-Learn Crash Course", "url": "https://www.youtube.com/watch?v=0B5eIE_1vpU", "duration": "1.5 hrs", "channel": "Nicholas Renotte"},
        ],
        "roadmap": ["Statistics Basics", "Supervised Learning", "Unsupervised Learning", "Model Evaluation", "Deployment"],
        "time": "8-12 weeks"
    },
    "deep learning": {
        "youtube": [
            {"title": "Deep Learning Specialization — Andrew Ng", "url": "https://www.youtube.com/watch?v=CS4cs9xVecg", "duration": "Full Course", "channel": "DeepLearning.AI"},
            {"title": "PyTorch Full Course", "url": "https://www.youtube.com/watch?v=V_xro1bcAuA", "duration": "6.5 hrs", "channel": "freeCodeCamp"},
        ],
        "roadmap": ["Neural Networks", "CNNs", "RNNs/LSTMs", "Transformers", "Model Deployment"],
        "time": "10-14 weeks"
    },
    "data analysis": {
        "youtube": [
            {"title": "Data Analysis with Python — freeCodeCamp", "url": "https://www.youtube.com/watch?v=r-uOLxNrNk8", "duration": "4 hrs", "channel": "freeCodeCamp"},
            {"title": "Pandas Tutorial — Corey Schafer", "url": "https://www.youtube.com/watch?v=ZyhVh-qRZPA", "duration": "3 hrs", "channel": "Corey Schafer"},
            {"title": "EDA Full Project Walkthrough", "url": "https://www.youtube.com/watch?v=Liv6eeb1VfE", "duration": "1.5 hrs", "channel": "Keith Galli"},
        ],
        "roadmap": ["Pandas & NumPy", "Data Cleaning", "EDA", "Visualization", "Statistical Analysis"],
        "time": "4-6 weeks"
    },
    "power bi": {
        "youtube": [
            {"title": "Power BI Full Course — Guy in a Cube", "url": "https://www.youtube.com/watch?v=AGrl-H87pRU", "duration": "5 hrs", "channel": "Guy in a Cube"},
            {"title": "Power BI for Beginners — Alex The Analyst", "url": "https://www.youtube.com/watch?v=ykvAWKML9Gk", "duration": "2 hrs", "channel": "Alex The Analyst"},
        ],
        "roadmap": ["Data Import & Transform", "DAX Basics", "Visualizations", "Reports & Dashboards", "Power Query"],
        "time": "3-5 weeks"
    },
    "tableau": {
        "youtube": [
            {"title": "Tableau Full Tutorial", "url": "https://www.youtube.com/watch?v=aHaOIvR00So", "duration": "3 hrs", "channel": "Simplilearn"},
            {"title": "Tableau for Beginners", "url": "https://www.youtube.com/watch?v=TPMlZxRRaBQ", "duration": "1.5 hrs", "channel": "Alex The Analyst"},
        ],
        "roadmap": ["Connecting Data", "Charts & Graphs", "Calculated Fields", "Dashboards", "Story Points"],
        "time": "3-4 weeks"
    },
    "javascript": {
        "youtube": [
            {"title": "JavaScript Full Course — freeCodeCamp", "url": "https://www.youtube.com/watch?v=PkZNo7MFNFg", "duration": "3.5 hrs", "channel": "freeCodeCamp"},
            {"title": "JavaScript — The Complete Guide", "url": "https://www.youtube.com/watch?v=W6NZfCO5SIk", "duration": "8 hrs", "channel": "Academind"},
        ],
        "roadmap": ["Syntax & DOM", "ES6+ Features", "Async/Await", "Fetch API", "Frameworks (React/Vue)"],
        "time": "6-8 weeks"
    },
    "react": {
        "youtube": [
            {"title": "React Full Course — freeCodeCamp", "url": "https://www.youtube.com/watch?v=bMknfKXIFA8", "duration": "12 hrs", "channel": "freeCodeCamp"},
            {"title": "React Hooks Crash Course", "url": "https://www.youtube.com/watch?v=O6P86uwfdR0", "duration": "2 hrs", "channel": "Web Dev Simplified"},
        ],
        "roadmap": ["JSX & Components", "State & Props", "Hooks", "React Router", "State Management"],
        "time": "6-8 weeks"
    },
    "dsa": {
        "youtube": [
            {"title": "DSA Full Course — freeCodeCamp", "url": "https://www.youtube.com/watch?v=8hly31xKli0", "duration": "8 hrs", "channel": "freeCodeCamp"},
            {"title": "Striver A2Z DSA Sheet", "url": "https://www.youtube.com/watch?v=0bHoB32fuj0", "duration": "Full Series", "channel": "take U forward"},
            {"title": "Love Babbar DSA Sheet", "url": "https://www.youtube.com/watch?v=WQoB2z67hvY", "duration": "Full Series", "channel": "Love Babbar"},
        ],
        "roadmap": ["Arrays & Strings", "Linked Lists", "Trees & Graphs", "DP & Recursion", "System Design"],
        "time": "12-16 weeks"
    },
    "statistics": {
        "youtube": [
            {"title": "Statistics for Data Science — Krish Naik", "url": "https://www.youtube.com/watch?v=LZzq1zSL1bs", "duration": "4 hrs", "channel": "Krish Naik"},
            {"title": "StatQuest Channel", "url": "https://www.youtube.com/@statquest", "duration": "Channel", "channel": "StatQuest"},
        ],
        "roadmap": ["Descriptive Stats", "Probability", "Distributions", "Hypothesis Testing", "Regression"],
        "time": "4-6 weeks"
    },
    "docker": {
        "youtube": [
            {"title": "Docker Crash Course — TechWorld with Nana", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE", "duration": "3.5 hrs", "channel": "TechWorld with Nana"},
        ],
        "roadmap": ["Containers vs VMs", "Dockerfile", "Images & Volumes", "Docker Compose", "Kubernetes Intro"],
        "time": "2-3 weeks"
    },
    "git": {
        "youtube": [
            {"title": "Git Full Course — freeCodeCamp", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk", "duration": "1 hr", "channel": "freeCodeCamp"},
        ],
        "roadmap": ["Init & Commit", "Branching", "Merging", "Remote Repos", "GitHub Workflows"],
        "time": "1-2 weeks"
    },
    "flask": {
        "youtube": [
            {"title": "Flask Full Tutorial — Tech With Tim", "url": "https://www.youtube.com/watch?v=mqhxxeeTbu0", "duration": "5 hrs", "channel": "Tech With Tim"},
            {"title": "Flask REST API — Traversy Media", "url": "https://www.youtube.com/watch?v=BSBRAnE59Yg", "duration": "1.5 hrs", "channel": "Traversy Media"},
        ],
        "roadmap": ["Routes & Templates", "Forms & DB", "Authentication", "REST APIs", "Deployment"],
        "time": "3-4 weeks"
    },
    "communication": {
        "youtube": [
            {"title": "Soft Skills for Placement — Unacademy", "url": "https://www.youtube.com/watch?v=nU7Q7E3CNMY", "duration": "2 hrs", "channel": "Unacademy"},
            {"title": "Group Discussion Tips", "url": "https://www.youtube.com/watch?v=xMHFvVwNUF0", "duration": "45 min", "channel": "Placement Gyaan"},
        ],
        "roadmap": ["Email Etiquette", "Interview Communication", "Group Discussion", "Presentation Skills", "Mock Interviews"],
        "time": "2-4 weeks"
    },
}

DSA_PATH = [
    {"week": "1-2",   "topic": "Arrays & Strings",           "problems": 25, "platform": "LeetCode"},
    {"week": "3-4",   "topic": "Linked Lists & Stacks/Queues","problems": 20, "platform": "GFG"},
    {"week": "5-6",   "topic": "Binary Trees & BST",          "problems": 30, "platform": "LeetCode"},
    {"week": "7-8",   "topic": "Graphs & BFS/DFS",            "problems": 25, "platform": "LeetCode"},
    {"week": "9-10",  "topic": "Dynamic Programming",         "problems": 30, "platform": "LeetCode"},
    {"week": "11-12", "topic": "Sorting, Searching & Greedy", "problems": 20, "platform": "GFG"},
    {"week": "13-16", "topic": "Revision + Mock Interviews",  "problems": 50, "platform": "InterviewBit"},
]


@recommend_bp.route('/')
@login_required
def index():
    # Latest skill gaps nikalo
    gap = SkillGap.query.filter_by(
        user_id=current_user.id
    ).order_by(SkillGap.analyzed_at.desc()).first()

    recommendations = []

    if gap:
        # missing_skills JSON parse karo
        try:
            missing = json.loads(gap.missing_skills) if gap.missing_skills else []
        except:
            missing = []

        seen = set()
        for item in missing:
            # item = {'skill': 'python', 'priority': 'critical'}
            if isinstance(item, dict):
                skill_name = item.get('skill', '').lower()
                priority = item.get('priority', 'normal')
            else:
                skill_name = str(item).lower()
                priority = 'normal'

            if skill_name in seen:
                continue
            seen.add(skill_name)

            # Priority map karo
            if priority == 'critical':
                p = 'High'
            elif priority == 'important':
                p = 'Medium'
            else:
                p = 'Low'

            resource = SKILL_RESOURCES.get(skill_name)
            if resource:
                recommendations.append({
                    "skill": skill_name.title(),
                    "priority": p,
                    "resource": resource
                })

    # Agar koi gap nahi toh default show karo
    if not recommendations:
        for skill in ["python", "sql", "dsa", "statistics", "communication"]:
            recommendations.append({
                "skill": skill.title(),
                "priority": "Medium",
                "resource": SKILL_RESOURCES[skill]
            })

    high_priority   = [r for r in recommendations if r['priority'] == 'High']
    medium_priority = [r for r in recommendations if r['priority'] == 'Medium']
    low_priority    = [r for r in recommendations if r['priority'] == 'Low']

    return render_template('recommendations/index.html',
                           recommendations=recommendations,
                           high_priority=high_priority,
                           medium_priority=medium_priority,
                           low_priority=low_priority,
                           dsa_path=DSA_PATH,
                           skill_resources=SKILL_RESOURCES)