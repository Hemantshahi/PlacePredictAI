"""
utils/skill_gap.py — Skill Gap Analysis Engine
MCE Placement Prediction System
"""

from typing import Dict, List, Tuple


# ─── Job Role Skill Requirements ──────────────────────────────────────────────
ROLE_SKILL_REQUIREMENTS = {

    # ── CSE / IT Roles ─────────────────────────────────────────────────────────
    "Software Engineer": {
        "critical":     ["python", "data structures", "algorithms", "oops", "sql", "git"],
        "important":    ["java", "c++", "javascript", "rest api", "linux", "system design"],
        "good_to_have": ["docker", "kubernetes", "aws", "react", "microservices", "agile"]
    },
    "Data Analyst": {
        "critical":     ["python", "sql", "excel", "power bi", "statistics"],
        "important":    ["pandas", "numpy", "tableau", "data visualization", "mysql"],
        "good_to_have": ["r", "matplotlib", "seaborn", "etl", "machine learning", "looker"]
    },
    "Data Scientist": {
        "critical":     ["python", "machine learning", "statistics", "sql", "pandas", "numpy"],
        "important":    ["scikit-learn", "deep learning", "nlp", "tensorflow", "feature engineering"],
        "good_to_have": ["pytorch", "computer vision", "xgboost", "docker", "flask", "spark"]
    },
    "Web Developer": {
        "critical":     ["html", "css", "javascript", "git"],
        "important":    ["react", "node.js", "bootstrap", "rest api", "sql"],
        "good_to_have": ["typescript", "mongodb", "docker", "aws", "graphql", "testing"]
    },
    "DevOps Engineer": {
        "critical":     ["linux", "docker", "git", "bash"],
        "important":    ["kubernetes", "jenkins", "aws", "ci/cd", "python"],
        "good_to_have": ["ansible", "terraform", "monitoring", "azure", "prometheus"]
    },
    "Android Developer": {
        "critical":     ["java", "kotlin", "android studio", "xml"],
        "important":    ["firebase", "rest api", "sqlite", "git", "mvvm"],
        "good_to_have": ["jetpack compose", "retrofit", "room", "material design", "testing"]
    },

    # ── ECE Roles ──────────────────────────────────────────────────────────────
    "Embedded Systems Engineer": {
        "critical":     ["c", "c++", "microcontrollers", "embedded c", "rtos"],
        "important":    ["arduino", "raspberry pi", "uart", "spi", "i2c", "pcb design"],
        "good_to_have": ["python", "matlab", "verilog", "fpga", "iot", "linux"]
    },
    "VLSI Design Engineer": {
        "critical":     ["verilog", "vhdl", "digital electronics", "logic design"],
        "important":    ["cadence", "synopsys", "fpga", "timing analysis", "dft"],
        "good_to_have": ["python", "tcl scripting", "functional verification", "upf"]
    },
    "RF & Communication Engineer": {
        "critical":     ["signal processing", "matlab", "digital communications", "antenna design"],
        "important":    ["python", "simulink", "spectrum analysis", "modulation techniques"],
        "good_to_have": ["labview", "hfss", "cst studio", "5g", "iot"]
    },
    "IoT Engineer": {
        "critical":     ["python", "c", "mqtt", "arduino", "raspberry pi"],
        "important":    ["aws iot", "azure iot", "rest api", "sensors", "linux"],
        "good_to_have": ["docker", "node.js", "machine learning", "firebase", "edge computing"]
    },

    # ── EEE Roles ──────────────────────────────────────────────────────────────
    "Electrical Engineer": {
        "critical":     ["circuit analysis", "power systems", "electrical machines", "matlab"],
        "important":    ["autocad electrical", "plc programming", "scada", "protection systems"],
        "good_to_have": ["python", "power electronics", "etap", "pscad", "renewable energy"]
    },
    "Power Systems Engineer": {
        "critical":     ["power systems", "load flow analysis", "fault analysis", "matlab"],
        "important":    ["etap", "pscad", "protection relay", "transformer design", "switchgear"],
        "good_to_have": ["python", "power electronics", "smart grid", "renewable energy", "scada"]
    },
    "Automation Engineer": {
        "critical":     ["plc programming", "scada", "hmi", "ladder logic"],
        "important":    ["siemens tia portal", "allen bradley", "instrumentation", "pid control"],
        "good_to_have": ["python", "industrial iot", "robotics", "drives & motors", "dcs"]
    },
    "Control Systems Engineer": {
        "critical":     ["control systems", "matlab", "simulink", "pid control"],
        "important":    ["plc", "python", "signal processing", "instrumentation"],
        "good_to_have": ["labview", "fpga", "robotics", "embedded systems", "scada"]
    },

    # ── Civil Roles ────────────────────────────────────────────────────────────
    "Civil Engineer": {
        "critical":     ["structural analysis", "autocad", "staad pro", "rcc design"],
        "important":    ["revit", "surveying", "quantity estimation", "construction management"],
        "good_to_have": ["ms project", "primavera", "gis", "bim", "etabs"]
    },
    "Structural Engineer": {
        "critical":     ["structural analysis", "staad pro", "etabs", "rcc design", "steel design"],
        "important":    ["autocad", "revit", "safe", "sap2000", "is codes"],
        "good_to_have": ["matlab", "python", "bim", "ansys", "abaqus"]
    },
    "Site Engineer": {
        "critical":     ["construction management", "autocad", "quantity surveying", "site supervision"],
        "important":    ["ms project", "surveying", "rcc design", "quality control"],
        "good_to_have": ["primavera", "revit", "gis", "bim", "safety management"]
    },
    "Transportation Engineer": {
        "critical":     ["highway design", "autocad", "traffic engineering", "pavement design"],
        "important":    ["civil 3d", "geometric design", "drainage design", "is codes"],
        "good_to_have": ["gis", "matlab", "traffic simulation", "infraworks", "synchro"]
    },
    "Environmental Engineer": {
        "critical":     ["water treatment", "environmental impact assessment", "autocad"],
        "important":    ["gis", "wastewater treatment", "solid waste management", "pollution control"],
        "good_to_have": ["python", "matlab", "remote sensing", "epanet", "hec-ras"]
    },

    # ── Mechanical Roles ───────────────────────────────────────────────────────
    "Mechanical Engineer": {
        "critical":     ["autocad", "solidworks", "catia", "engineering drawing"],
        "important":    ["ansys", "manufacturing processes", "thermodynamics", "fluid mechanics"],
        "good_to_have": ["matlab", "python", "creo", "nx", "gd&t", "lean manufacturing"]
    },
    "Design Engineer": {
        "critical":     ["solidworks", "catia", "autocad", "gd&t", "engineering drawing"],
        "important":    ["ansys", "creo", "nx", "fea", "product design"],
        "good_to_have": ["matlab", "python", "3d printing", "dfma", "plm tools"]
    },
    "Production Engineer": {
        "critical":     ["manufacturing processes", "autocad", "quality control", "lean manufacturing"],
        "important":    ["cnc programming", "solidworks", "six sigma", "erp", "production planning"],
        "good_to_have": ["python", "matlab", "industry 4.0", "automation", "kaizen"]
    },
    "Thermal Engineer": {
        "critical":     ["thermodynamics", "heat transfer", "fluid mechanics", "matlab"],
        "important":    ["ansys fluent", "cfd", "hvac design", "solidworks"],
        "good_to_have": ["python", "openfoam", "comsol", "energy simulation", "renewable energy"]
    },
    "Automobile Engineer": {
        "critical":     ["catia", "solidworks", "autocad", "vehicle dynamics"],
        "important":    ["ansys", "engine design", "transmission systems", "matlab"],
        "good_to_have": ["matlab simulink", "cfd", "electric vehicles", "embedded systems", "creo"]
    },
}

# ─── Learning Resources ────────────────────────────────────────────────────────
SKILL_RESOURCES = {
    "python": [
        {"title": "Python Full Course - freeCodeCamp", "url": "https://youtube.com/watch?v=rfscVS0vtbw", "platform": "YouTube"},
        {"title": "Python for Everybody - Coursera", "url": "https://coursera.org/specializations/python", "platform": "Coursera"},
    ],
    "sql": [
        {"title": "SQL Tutorial - W3Schools", "url": "https://www.w3schools.com/sql/", "platform": "Web"},
        {"title": "MySQL Full Course - Mosh", "url": "https://youtube.com/watch?v=7S_tz1z_5bA", "platform": "YouTube"},
    ],
    "machine learning": [
        {"title": "ML Course - Andrew Ng", "url": "https://coursera.org/learn/machine-learning", "platform": "Coursera"},
        {"title": "ML A-Z - Krish Naik", "url": "https://youtube.com/watch?v=GwIo3gDZCVQ", "platform": "YouTube"},
    ],
    "data structures": [
        {"title": "DSA Full Course - Abdul Bari", "url": "https://youtube.com/watch?v=0IAPZzGSbME", "platform": "YouTube"},
        {"title": "LeetCode Practice", "url": "https://leetcode.com", "platform": "Practice"},
    ],
    "autocad": [
        {"title": "AutoCAD Full Course - Beginner", "url": "https://youtube.com/watch?v=J8UJdCd4bj8", "platform": "YouTube"},
        {"title": "AutoCAD Tutorial - Autodesk", "url": "https://www.autodesk.com/learning", "platform": "Web"},
    ],
    "solidworks": [
        {"title": "SolidWorks Full Tutorial", "url": "https://youtube.com/watch?v=6dA09k-7Rpc", "platform": "YouTube"},
        {"title": "SolidWorks Official Tutorials", "url": "https://my.solidworks.com", "platform": "Web"},
    ],
    "matlab": [
        {"title": "MATLAB Tutorial for Beginners", "url": "https://youtube.com/watch?v=T_ekAD7U-wU", "platform": "YouTube"},
        {"title": "MATLAB Onramp - MathWorks", "url": "https://matlabacademy.mathworks.com", "platform": "Web"},
    ],
    "staad pro": [
        {"title": "STAAD Pro Full Course", "url": "https://youtube.com/watch?v=YqjD2LGTLWI", "platform": "YouTube"},
    ],
    "ansys": [
        {"title": "ANSYS Tutorial for Beginners", "url": "https://youtube.com/watch?v=fFnFdLNmTz0", "platform": "YouTube"},
        {"title": "ANSYS Learning Hub", "url": "https://courses.ansys.com", "platform": "Web"},
    ],
    "plc programming": [
        {"title": "PLC Programming for Beginners", "url": "https://youtube.com/watch?v=fJAkikhFE4U", "platform": "YouTube"},
    ],
    "catia": [
        {"title": "CATIA V5 Tutorial Beginners", "url": "https://youtube.com/watch?v=3A-4V4b8V4s", "platform": "YouTube"},
    ],
    "power systems": [
        {"title": "Power Systems - NPTEL", "url": "https://nptel.ac.in/courses/108", "platform": "NPTEL"},
    ],
    "verilog": [
        {"title": "Verilog HDL Tutorial", "url": "https://youtube.com/watch?v=PJGvZSlsLKs", "platform": "YouTube"},
    ],
    "default": [
        {"title": "Search on YouTube", "url": "https://youtube.com", "platform": "YouTube"},
        {"title": "Search on Coursera", "url": "https://coursera.org", "platform": "Coursera"},
        {"title": "NPTEL Free Courses", "url": "https://nptel.ac.in", "platform": "NPTEL"},
    ]
}

# ─── Branch to Default Role Mapping ───────────────────────────────────────────
BRANCH_DEFAULT_ROLES = {
    "CSE":      "Software Engineer",
    "CSE-AI":   "Data Scientist",
    "CSE (AI)": "Data Scientist",
    "CSE-DS":   "Data Analyst",
    "CSE (DS)": "Data Analyst",
    "IT":       "Software Engineer",
    "ECE":      "Embedded Systems Engineer",
    "EEE":      "Electrical Engineer",
    "Civil":    "Civil Engineer",
    "Civil-CA": "Civil Engineer",
    "CE":       "Civil Engineer",
    "ME":       "Mechanical Engineer",
}

# ─── Company Database ──────────────────────────────────────────────────────────
COMPANY_DATABASE = [

    # ── CSE / IT Companies ─────────────────────────────────────────────────────
    {"name": "Google",      "tier": "Tier 1", "package": "20–40 LPA", "min_cgpa": 8.0,
     "required_skills": ["python", "data structures", "algorithms", "system design"],
     "domain": "Tech", "branches": ["CSE", "CSE-AI", "CSE-DS", "IT", "ECE"]},

    {"name": "Microsoft",   "tier": "Tier 1", "package": "20–35 LPA", "min_cgpa": 7.5,
     "required_skills": ["python", "c++", "data structures", "algorithms", "azure"],
     "domain": "Tech", "branches": ["CSE", "CSE-AI", "CSE-DS", "IT", "ECE"]},

    {"name": "Amazon",      "tier": "Tier 1", "package": "18–30 LPA", "min_cgpa": 7.0,
     "required_skills": ["python", "java", "data structures", "algorithms", "aws"],
     "domain": "Tech", "branches": ["CSE", "CSE-AI", "CSE-DS", "IT", "ECE"]},

    {"name": "TCS",         "tier": "Service", "package": "3.5–7 LPA", "min_cgpa": 6.0,
     "required_skills": ["python", "java", "sql", "c"],
     "domain": "IT Services", "branches": ["CSE", "CSE-AI", "CSE-DS", "IT", "ECE", "EEE", "ME", "Civil"]},

    {"name": "Infosys",     "tier": "Service", "package": "3.6–8 LPA", "min_cgpa": 6.0,
     "required_skills": ["python", "java", "sql", "oops"],
     "domain": "IT Services", "branches": ["CSE", "CSE-AI", "CSE-DS", "IT", "ECE", "EEE", "ME", "Civil"]},

    {"name": "Wipro",       "tier": "Service", "package": "3.5–7 LPA", "min_cgpa": 6.0,
     "required_skills": ["python", "c", "java", "sql"],
     "domain": "IT Services", "branches": ["CSE", "CSE-AI", "CSE-DS", "IT", "ECE", "EEE", "ME", "Civil"]},

    {"name": "Cognizant",   "tier": "Service", "package": "4–8 LPA",   "min_cgpa": 6.0,
     "required_skills": ["python", "java", "sql", "html"],
     "domain": "IT Services", "branches": ["CSE", "CSE-AI", "CSE-DS", "IT", "ECE"]},

    {"name": "Accenture",   "tier": "Service", "package": "4.5–9 LPA", "min_cgpa": 6.0,
     "required_skills": ["python", "sql", "power bi", "excel"],
     "domain": "Consulting", "branches": ["CSE", "CSE-AI", "CSE-DS", "IT", "ECE", "EEE", "ME", "Civil"]},

    {"name": "Mu Sigma",    "tier": "Analytics", "package": "5–10 LPA", "min_cgpa": 6.0,
     "required_skills": ["python", "statistics", "sql", "excel", "data visualization"],
     "domain": "Analytics", "branches": ["CSE", "CSE-AI", "CSE-DS", "IT"]},

    {"name": "Fractal Analytics", "tier": "Analytics", "package": "6–12 LPA", "min_cgpa": 6.5,
     "required_skills": ["python", "machine learning", "statistics", "sql"],
     "domain": "Analytics", "branches": ["CSE", "CSE-AI", "CSE-DS"]},

    {"name": "EXL Service", "tier": "Analytics", "package": "5–10 LPA", "min_cgpa": 6.0,
     "required_skills": ["python", "sql", "excel", "power bi", "statistics"],
     "domain": "Analytics", "branches": ["CSE", "CSE-AI", "CSE-DS", "IT"]},

    # ── EEE Companies ──────────────────────────────────────────────────────────
    {"name": "BHEL",        "tier": "PSU", "package": "7–12 LPA", "min_cgpa": 6.5,
     "required_skills": ["power systems", "electrical machines", "matlab", "plc programming"],
     "domain": "Power & Energy", "branches": ["EEE", "ECE", "ME"]},

    {"name": "NTPC",        "tier": "PSU", "package": "8–14 LPA", "min_cgpa": 6.5,
     "required_skills": ["power systems", "electrical machines", "scada", "protection systems"],
     "domain": "Power Generation", "branches": ["EEE", "ME", "Civil"]},

    {"name": "PGCIL",       "tier": "PSU", "package": "8–13 LPA", "min_cgpa": 6.5,
     "required_skills": ["power systems", "transmission systems", "scada", "protection relay"],
     "domain": "Power Transmission", "branches": ["EEE"]},

    {"name": "Siemens",     "tier": "MNC", "package": "6–14 LPA", "min_cgpa": 6.5,
     "required_skills": ["plc programming", "scada", "automation", "electrical machines"],
     "domain": "Automation", "branches": ["EEE", "ECE", "ME"]},

    {"name": "ABB India",   "tier": "MNC", "package": "6–13 LPA", "min_cgpa": 6.5,
     "required_skills": ["power systems", "automation", "plc programming", "drives & motors"],
     "domain": "Power & Automation", "branches": ["EEE", "ECE", "ME"]},

    {"name": "L&T ECC",     "tier": "Tier 1", "package": "5–10 LPA", "min_cgpa": 6.0,
     "required_skills": ["electrical machines", "autocad electrical", "power systems"],
     "domain": "EPC", "branches": ["EEE", "Civil", "ME"]},

    {"name": "Tata Power",  "tier": "Tier 2", "package": "6–11 LPA", "min_cgpa": 6.5,
     "required_skills": ["power systems", "electrical machines", "scada", "renewable energy"],
     "domain": "Power", "branches": ["EEE", "ME"]},

    # ── Civil Companies ────────────────────────────────────────────────────────
    {"name": "L&T Construction", "tier": "Tier 1", "package": "5–10 LPA", "min_cgpa": 6.0,
     "required_skills": ["autocad", "staad pro", "construction management", "surveying"],
     "domain": "Construction", "branches": ["Civil", "Civil-CA", "ME"]},

    {"name": "NHAI",        "tier": "PSU", "package": "7–12 LPA", "min_cgpa": 6.5,
     "required_skills": ["highway design", "autocad", "quantity surveying", "traffic engineering"],
     "domain": "Roads & Highways", "branches": ["Civil", "Civil-CA"]},

    {"name": "RITES Ltd",   "tier": "PSU", "package": "7–11 LPA", "min_cgpa": 6.5,
     "required_skills": ["structural analysis", "autocad", "construction management"],
     "domain": "Infrastructure", "branches": ["Civil", "Civil-CA", "ME"]},

    {"name": "Shapoorji Pallonji", "tier": "Tier 1", "package": "5–9 LPA", "min_cgpa": 6.0,
     "required_skills": ["autocad", "construction management", "quantity surveying", "site supervision"],
     "domain": "Construction", "branches": ["Civil", "Civil-CA"]},

    {"name": "Afcons Infrastructure", "tier": "Tier 2", "package": "5–9 LPA", "min_cgpa": 6.0,
     "required_skills": ["autocad", "staad pro", "construction management", "surveying"],
     "domain": "Infrastructure", "branches": ["Civil", "Civil-CA"]},

    {"name": "NBCC India",  "tier": "PSU", "package": "7–11 LPA", "min_cgpa": 6.5,
     "required_skills": ["structural analysis", "autocad", "rcc design", "quantity estimation"],
     "domain": "Construction", "branches": ["Civil", "Civil-CA"]},

    # ── Mechanical Companies ───────────────────────────────────────────────────
    {"name": "Tata Motors", "tier": "Tier 1", "package": "5–10 LPA", "min_cgpa": 6.0,
     "required_skills": ["solidworks", "catia", "autocad", "manufacturing processes"],
     "domain": "Automobile", "branches": ["ME", "EEE", "ECE"]},

    {"name": "Maruti Suzuki", "tier": "Tier 1", "package": "5–10 LPA", "min_cgpa": 6.0,
     "required_skills": ["autocad", "solidworks", "production planning", "quality control"],
     "domain": "Automobile", "branches": ["ME", "EEE"]},

    {"name": "Bosch India", "tier": "MNC", "package": "6–12 LPA", "min_cgpa": 6.5,
     "required_skills": ["solidworks", "catia", "autocad", "manufacturing processes", "matlab"],
     "domain": "Auto Components", "branches": ["ME", "ECE", "EEE"]},

    {"name": "Bajaj Auto",  "tier": "Tier 1", "package": "5–10 LPA", "min_cgpa": 6.0,
     "required_skills": ["autocad", "catia", "manufacturing processes", "quality control"],
     "domain": "Automobile", "branches": ["ME", "EEE"]},

    {"name": "ISRO",        "tier": "PSU", "package": "8–14 LPA", "min_cgpa": 7.5,
     "required_skills": ["matlab", "solidworks", "ansys", "control systems", "thermodynamics"],
     "domain": "Space & Defence", "branches": ["ME", "ECE", "EEE", "CSE"]},

    {"name": "DRDO",        "tier": "PSU", "package": "7–13 LPA", "min_cgpa": 7.0,
     "required_skills": ["matlab", "c", "c++", "embedded systems", "signal processing"],
     "domain": "Defence", "branches": ["ME", "ECE", "EEE", "CSE"]},

    {"name": "Mahindra",    "tier": "Tier 1", "package": "5–10 LPA", "min_cgpa": 6.0,
     "required_skills": ["solidworks", "autocad", "manufacturing processes", "quality control"],
     "domain": "Automobile", "branches": ["ME", "EEE"]},
]


def _normalize_branch(branch: str) -> str:
    """Normalize branch name for comparison."""
    return branch.strip().upper().replace(' ', '-').replace('(', '').replace(')', '')

def recommend_companies(
    user_skills: List[str],
    cgpa: float,
    prediction_score: float,
    user_branch: str = None
) -> List[Dict]:
    """Return companies matched to user profile with match %."""
    user_skills_lower = [s.lower() for s in user_skills]
    results = []

    # Branch normalize karo
    user_branch_norm = _normalize_branch(user_branch) if user_branch else None

    for company in COMPANY_DATABASE:
        # CGPA check
        if cgpa < company['min_cgpa']:
            continue

        # Branch filter
        if user_branch_norm and 'branches' in company:
            company_branches_norm = [_normalize_branch(b) for b in company['branches']]
            if user_branch_norm not in company_branches_norm:
                continue

        required = [s.lower() for s in company['required_skills']]
        matched = sum(
            1 for skill in required
            if any(skill in u or u in skill for u in user_skills_lower)
        )
        match_pct = round((matched / len(required)) * 100) if required else 0

        if match_pct >= 25:
            results.append({
                'name':            company['name'],
                'tier':            company['tier'],
                'package':         company['package'],
                'domain':          company['domain'],
                'match_percentage': match_pct,
                'min_cgpa':        company['min_cgpa'],
                'required_skills': company['required_skills'],
            })

    results.sort(key=lambda x: x['match_percentage'], reverse=True)
    return results[:12]


class SkillGapAnalyzer:
    """Analyzes skill gaps between user skills and job role requirements."""

    def analyze(self, user_skills: List[str], job_role: str) -> Dict:
        user_skills_lower = [s.lower().strip() for s in user_skills]
        requirements = ROLE_SKILL_REQUIREMENTS.get(
            job_role, ROLE_SKILL_REQUIREMENTS["Software Engineer"]
        )

        gap_data    = {'critical': [], 'important': [], 'good_to_have': []}
        present_skills = []
        all_missing    = []

        for priority, skills_list in requirements.items():
            for skill in skills_list:
                skill_lower = skill.lower()
                has_skill = any(
                    skill_lower in u or u in skill_lower
                    for u in user_skills_lower
                )
                if has_skill:
                    present_skills.append(skill)
                else:
                    gap_data[priority].append(skill)
                    all_missing.append({'skill': skill, 'priority': priority})

        recommendations = self._build_recommendations(gap_data)

        total_required = sum(len(v) for v in requirements.values())
        matched        = total_required - len(all_missing)
        match_pct      = round((matched / total_required) * 100, 1) if total_required else 0

        if match_pct >= 80:
            readiness, readiness_color = "High",   "#22c55e"
        elif match_pct >= 55:
            readiness, readiness_color = "Medium", "#f59e0b"
        else:
            readiness, readiness_color = "Low",    "#ef4444"

        return {
            'job_role':        job_role,
            'present_skills':  present_skills,
            'missing_skills':  all_missing,
            'gap_breakdown':   gap_data,
            'recommendations': recommendations,
            'match_percentage': match_pct,
            'readiness':        readiness,
            'readiness_color':  readiness_color,
        }

    def _build_recommendations(self, gap_data: Dict) -> List[Dict]:
        recs = []
        for priority in ['critical', 'important', 'good_to_have']:
            for skill in gap_data.get(priority, [])[:3]:
                resources = SKILL_RESOURCES.get(skill.lower(), SKILL_RESOURCES['default'])
                recs.append({
                    'skill':          skill,
                    'priority':       priority,
                    'resources':      resources[:2],
                    'estimated_time': self._estimate_time(priority)
                })
        return recs

    def _estimate_time(self, priority: str) -> str:
        return {
            'critical':     '2–4 weeks',
            'important':    '1–2 weeks',
            'good_to_have': '3–7 days'
        }.get(priority, '1 week')


# ─── Singletons ────────────────────────────────────────────────────────────────
skill_gap_analyzer = SkillGapAnalyzer()