"""
utils/ats_scorer.py — Enhanced ATS Resume Scoring Engine
MCE Placement Prediction System
"""

import re
import json
from typing import Dict, List, Tuple


# ─── Job Role Keyword Bank ─────────────────────────────────────────────────────
JOB_KEYWORDS = {
    "Software Engineer": [
        "python", "java", "c++", "javascript", "react", "node", "django", "flask",
        "sql", "git", "github", "rest api", "microservices", "docker", "kubernetes",
        "data structures", "algorithms", "oops", "agile", "scrum", "linux",
        "machine learning", "cloud", "aws", "system design", "api"
    ],
    "Data Analyst": [
        "python", "sql", "excel", "power bi", "tableau", "pandas", "numpy",
        "matplotlib", "seaborn", "statistics", "data visualization", "etl",
        "mysql", "postgresql", "r", "regression", "hypothesis testing", "dashboard",
        "data cleaning", "business intelligence", "analytics", "reporting"
    ],
    "Data Scientist": [
        "python", "machine learning", "deep learning", "tensorflow", "pytorch",
        "scikit-learn", "nlp", "computer vision", "statistics", "sql", "pandas",
        "numpy", "feature engineering", "model deployment", "flask", "docker",
        "xgboost", "random forest", "neural network", "regression", "classification"
    ],
    "Web Developer": [
        "html", "css", "javascript", "react", "vue", "angular", "node.js",
        "express", "bootstrap", "tailwind", "php", "mysql", "mongodb", "rest api",
        "git", "github", "responsive design", "jquery", "typescript", "api"
    ],
    "DevOps Engineer": [
        "linux", "docker", "kubernetes", "jenkins", "ci/cd", "ansible", "terraform",
        "aws", "azure", "gcp", "bash", "python", "git", "monitoring", "prometheus",
        "grafana", "nginx", "cloud", "infrastructure", "automation"
    ],
    "Android Developer": [
        "java", "kotlin", "android studio", "xml", "firebase", "rest api",
        "sqlite", "room", "retrofit", "mvvm", "git", "material design",
        "recyclerview", "fragments", "navigation", "jetpack compose"
    ],
    "Embedded Systems Engineer": [
        "c", "c++", "embedded c", "microcontrollers", "rtos", "arduino",
        "raspberry pi", "uart", "spi", "i2c", "pcb design", "matlab",
        "verilog", "fpga", "iot", "linux", "firmware"
    ],
    "Electrical Engineer": [
        "matlab", "simulink", "plc", "scada", "power systems", "autocad",
        "electrical machines", "circuit analysis", "protection systems",
        "python", "labview", "etap", "power electronics"
    ],
    "Civil Engineer": [
        "autocad", "staad pro", "revit", "structural analysis", "rcc design",
        "surveying", "construction management", "quantity estimation",
        "ms project", "primavera", "bim", "gis", "etabs"
    ],
    "Mechanical Engineer": [
        "autocad", "solidworks", "catia", "ansys", "creo", "matlab",
        "manufacturing processes", "thermodynamics", "fluid mechanics",
        "gd&t", "fea", "cfd", "engineering drawing", "nx"
    ],
}

# ─── Mandatory Resume Sections ─────────────────────────────────────────────────
REQUIRED_SECTIONS = [
    "education", "skills", "projects", "experience",
    "certifications", "contact", "summary", "objective"
]

# ─── ATS Format Signals ───────────────────────────────────────────────────────
GOOD_FORMAT_SIGNALS = [
    r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b',
    r'\d{4}',
    r'[\w\.-]+@[\w\.-]+\.\w+',
    r'\+?\d[\d\s\-]{8,}',
    r'linkedin\.com',
    r'github\.com',
    r'\b(gpa|cgpa|percentage)\b',
    r'\b(present|current)\b',
    r'\d+\s*%',
]

BAD_FORMAT_SIGNALS = [
    r'\t{3,}',
    r' {5,}',
]

# ─── Action Verbs ──────────────────────────────────────────────────────────────
STRONG_ACTION_VERBS = [
    "developed", "built", "designed", "implemented", "created", "deployed",
    "optimized", "improved", "reduced", "increased", "managed", "led",
    "collaborated", "analyzed", "researched", "automated", "integrated",
    "trained", "evaluated", "architected", "maintained", "delivered",
    "achieved", "spearheaded", "streamlined", "engineered", "launched",
    "established", "coordinated", "executed", "transformed"
]


class ATSScorer:
    """
    Enhanced ATS Scoring Engine:
    - Keyword matching    (35%) — Job-specific keywords
    - Section completeness(25%) — Required sections present
    - Format & Quality    (20%) — Dates, links, structure
    - Contact info        (10%) — Email, phone, LinkedIn, GitHub
    - Content quality     (10%) — Action verbs, quantified results
    """

    def __init__(self):
        self.weights = {
            'keyword':  35,
            'sections': 25,
            'format':   20,
            'contact':  10,
            'quality':  10,
        }

    def score(self, resume_text: str, job_role: str = "Software Engineer") -> Dict:
        """Returns enhanced ATS scoring breakdown with suggestions."""
        text_lower = resume_text.lower()
        suggestions = []

        # 1. Keyword Score (0-100)
        kw_score, kw_details, kw_sugg = self._keyword_score(text_lower, job_role)
        suggestions.extend(kw_sugg)

        # 2. Section Score (0-100)
        sec_score, sec_details, sec_sugg = self._section_score(text_lower)
        suggestions.extend(sec_sugg)

        # 3. Format Score (0-100)
        fmt_score, fmt_details, fmt_sugg = self._format_score(resume_text, text_lower)
        suggestions.extend(fmt_sugg)

        # 4. Contact Score (0-100)
        con_score, con_details, con_sugg = self._contact_score(resume_text)
        suggestions.extend(con_sugg)

        # 5. Content Quality Score (0-100) — NEW!
        qual_score, qual_details, qual_sugg = self._quality_score(resume_text, text_lower)
        suggestions.extend(qual_sugg)

        # Cap all scores
        kw_score   = min(max(kw_score, 0), 100)
        sec_score  = min(max(sec_score, 0), 100)
        fmt_score  = min(max(fmt_score, 0), 100)
        con_score  = min(max(con_score, 0), 100)
        qual_score = min(max(qual_score, 0), 100)

        # Weighted total
        total = round(
            (kw_score   * 0.35) +
            (sec_score  * 0.25) +
            (fmt_score  * 0.20) +
            (con_score  * 0.10) +
            (qual_score * 0.10),
            1
        )
        total = min(total, 100)

        # Display scores (scaled to max)
        kw_display   = round(kw_score   * 35 / 100, 1)  # /35
        sec_display  = round(sec_score  * 25 / 100, 1)  # /25
        fmt_display  = round(fmt_score  * 20 / 100, 1)  # /20
        con_display  = round(con_score  * 10 / 100, 1)  # /10
        qual_display = round(qual_score * 10 / 100, 1)  # /10

        # Rating
        if total >= 80:
            rating, color = "Excellent", "#16a34a"
        elif total >= 65:
            rating, color = "Good",      "#2563eb"
        elif total >= 45:
            rating, color = "Average",   "#f59e0b"
        else:
            rating, color = "Needs Work","#ef4444"

        # Matched keywords for display
        matched_kw = kw_details.get('found', [])

        return {
            'total_score': total,
            'rating':      rating,
            'color':       color,
            'breakdown': {
                'keyword_score':  kw_display,
                'section_score':  sec_display,
                'format_score':   fmt_display,
                'contact_score':  con_display,
                'quality_score':  qual_display,
            },
            'keyword_details':  kw_details,
            'section_details':  sec_details,
            'format_details':   fmt_details,
            'contact_details':  con_details,
            'quality_details':  qual_details,
            'matched_keywords': matched_kw,
            'suggestions':      self._prioritize_suggestions(suggestions)[:10],
        }

    # ── 1. Keyword Score ───────────────────────────────────────────────────────

    def _keyword_score(self, text: str, role: str) -> Tuple[float, Dict, List]:
        keywords = JOB_KEYWORDS.get(role, JOB_KEYWORDS["Software Engineer"])
        found   = [kw for kw in keywords if kw in text]
        missing = [kw for kw in keywords if kw not in text]
        score   = (len(found) / len(keywords)) * 100

        suggestions = []
        if missing:
            critical = missing[:4]
            suggestions.append(
                f"🔑 Add these important keywords for {role}: "
                f"{', '.join(critical)}"
            )
        if len(found) < len(keywords) * 0.5:
            suggestions.append(
                f"⚠️ Only {len(found)}/{len(keywords)} required keywords found. "
                f"Tailor your resume for {role}."
            )

        return score, {'found': found, 'missing': missing, 'total': len(keywords)}, suggestions

    # ── 2. Section Score ───────────────────────────────────────────────────────

    def _section_score(self, text: str) -> Tuple[float, Dict, List]:
        found   = []
        missing = []

        for section in REQUIRED_SECTIONS:
            pattern = r'\b' + section + r'\b'
            if re.search(pattern, text, re.I):
                found.append(section)
            else:
                missing.append(section)

        score = (len(found) / len(REQUIRED_SECTIONS)) * 100
        suggestions = []

        # Priority missing sections
        priority_missing = [s for s in missing if s in
                           ['education', 'skills', 'experience', 'projects']]
        for sec in priority_missing[:2]:
            suggestions.append(
                f"📋 Add a dedicated '{sec.title()}' section — it's critical for ATS."
            )

        return score, {'found': found, 'missing': missing}, suggestions

    # ── 3. Format Score ────────────────────────────────────────────────────────

    def _format_score(self, text: str, text_lower: str) -> Tuple[float, Dict, List]:
        good_hits = sum(
            1 for p in GOOD_FORMAT_SIGNALS
            if re.search(p, text_lower, re.IGNORECASE)
        )
        bad_hits = sum(
            1 for p in BAD_FORMAT_SIGNALS
            if re.search(p, text)
        )

        # Word count check
        word_count = len(text.split())
        if word_count < 200:
            bad_hits += 2
        elif word_count > 1000:
            bad_hits += 1

        score = min(100, (good_hits / len(GOOD_FORMAT_SIGNALS)) * 100)
        score = max(0, score - bad_hits * 8)

        details = {
            'good_signals': good_hits,
            'bad_signals': bad_hits,
            'word_count': word_count,
        }

        suggestions = []
        if not re.search(r'linkedin\.com', text_lower):
            suggestions.append(
                "🔗 Add your LinkedIn URL — many ATS systems check for it."
            )
        if not re.search(r'github\.com', text_lower):
            suggestions.append(
                "💻 Add your GitHub URL — showcases your technical work."
            )
        if not re.search(r'\d{4}', text):
            suggestions.append(
                "📅 Add dates to your experience and education sections."
            )
        if word_count < 250:
            suggestions.append(
                f"📝 Resume is too short ({word_count} words). Aim for 400-700 words."
            )
        if word_count > 900:
            suggestions.append(
                f"✂️ Resume is too long ({word_count} words). Keep it under 700 words for freshers."
            )

        return score, details, suggestions

    # ── 4. Contact Score ───────────────────────────────────────────────────────

    def _contact_score(self, text: str) -> Tuple[float, Dict, List]:
        checks = {
            'email':    bool(re.search(r'[\w\.\-]+@[\w\.\-]+\.\w+', text)),
            'phone':    bool(re.search(r'\+?\d[\d\s\-]{8,}', text)),
            'linkedin': bool(re.search(r'linkedin\.com', text, re.I)),
            'github':   bool(re.search(r'github\.com', text, re.I)),
            'location': bool(re.search(
                r'\b(bihar|patna|motihari|delhi|mumbai|bangalore|'
                r'bengaluru|hyderabad|chennai|india|noida|gurgaon)\b',
                text, re.I
            )),
        }
        score = (sum(checks.values()) / len(checks)) * 100
        suggestions = []
        labels = {
            'email':    'Email address',
            'phone':    'Phone number',
            'linkedin': 'LinkedIn profile URL',
            'github':   'GitHub profile URL',
            'location': 'Location/City',
        }
        for k, v in checks.items():
            if not v:
                suggestions.append(f"📞 Add your {labels[k]} to the contact section.")

        return score, checks, suggestions

    # ── 5. Content Quality Score (NEW!) ───────────────────────────────────────

    def _quality_score(self, text: str, text_lower: str) -> Tuple[float, Dict, List]:
        """
        Check content quality:
        - Action verbs used
        - Quantified achievements
        - No spelling of "responsible for" (weak phrase)
        - No first-person pronouns
        """
        score = 0
        details = {}
        suggestions = []

        # Action verbs check (40 points)
        verbs_found = [v for v in STRONG_ACTION_VERBS if v in text_lower]
        verb_score  = min(40, len(verbs_found) * 4)
        score += verb_score
        details['action_verbs'] = verbs_found[:8]
        details['action_verb_count'] = len(verbs_found)

        if len(verbs_found) < 5:
            suggestions.append(
                f"💪 Use more action verbs (found {len(verbs_found)}). "
                f"Try: developed, optimized, implemented, designed..."
            )

        # Quantified achievements (30 points)
        quant_patterns = [
            r'\d+\s*%',
            r'\d+\s*(x|times|fold)',
            r'\d+\s*(users|students|records|requests)',
            r'(reduced|improved|increased|optimized).{0,30}\d+',
        ]
        quant_count = sum(
            1 for p in quant_patterns
            if re.search(p, text, re.I)
        )
        quant_score = min(30, quant_count * 10)
        score += quant_score
        details['quantified_results'] = quant_count > 0

        if quant_count == 0:
            suggestions.append(
                "📊 Add quantified achievements (e.g., 'Reduced load time by 30%', "
                "'Built model with 87% accuracy')."
            )

        # Weak phrases check (-15 each)
        weak_phrases = [
            r'responsible for',
            r'worked on',
            r'helped with',
            r'assisted in',
            r'involved in',
        ]
        weak_count = sum(
            1 for p in weak_phrases
            if re.search(p, text_lower)
        )
        if weak_count > 0:
            score -= weak_count * 5
            suggestions.append(
                f"🔄 Replace weak phrases like 'responsible for', 'worked on' "
                f"with strong action verbs."
            )

        # First person pronouns (bad for ATS)
        pronouns = re.findall(r'\b(i |i\'m|my |me |myself)\b', text_lower)
        if len(pronouns) > 3:
            score -= 10
            suggestions.append(
                "👤 Avoid using first-person pronouns (I, my, me) in resume."
            )

        # Length check (30 points)
        word_count = len(text.split())
        if 300 <= word_count <= 700:
            score += 30
        elif 200 <= word_count < 300 or 700 < word_count <= 900:
            score += 15

        details['word_count']   = word_count
        details['weak_phrases'] = weak_count

        score = min(max(score, 0), 100)
        return score, details, suggestions

    # ── Suggestion Prioritizer ─────────────────────────────────────────────────

    def _prioritize_suggestions(self, suggestions: List[str]) -> List[str]:
        """Remove duplicates and prioritize critical suggestions."""
        seen = set()
        unique = []
        for s in suggestions:
            key = s[:40]
            if key not in seen:
                seen.add(key)
                unique.append(s)

        # Critical first (🔑, 📋, ⚠️), then others
        critical = [s for s in unique if s.startswith(('🔑', '📋', '⚠️'))]
        others   = [s for s in unique if not s.startswith(('🔑', '📋', '⚠️'))]
        return critical + others


# ─── Singleton ─────────────────────────────────────────────────────────────────
ats_scorer = ATSScorer()
