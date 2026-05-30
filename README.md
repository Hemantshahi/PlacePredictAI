# 🎓 PlacePredict AI
## Smart Placement Prediction, ATS Resume Scoring & Skill Gap Analysis System
### Motihari College of Engineering — Training & Placement Cell

---

## 📌 Project Overview

PlacePredict AI is a full-stack AI-powered placement prediction system built for **MCE Motihari's T&P Cell**. It combines:

- ✅ **ATS Resume Scoring** (0–100 with suggestions)
- ✅ **ML Placement Prediction** (Random Forest + XGBoost + ANN Ensemble)
- ✅ **Skill Gap Analysis** with YouTube learning resources
- ✅ **Company Matching** (TCS, Infosys, Google, Mu Sigma + 10 more)
- ✅ **AI Career Chatbot** (PlaceBot powered by Claude AI)
- ✅ **Admin Dashboard** with analytics charts
- ✅ **PDF/DOC Resume Parser** using NLP

---

## 📁 Project Structure

```
PlacePredictPro/
├── app.py                        # Flask app factory + entry point
├── requirements.txt              # Python dependencies
├── database_setup.sql            # MySQL setup script
├── .env                          # Environment variables (create this)
│
├── config/
│   └── config.py                 # App configuration
│
├── models/
│   ├── models.py                 # SQLAlchemy DB models
│   ├── train_model.py            # ML training script (run once)
│   └── saved/                    # Trained model files (auto-generated)
│
├── routes/
│   ├── auth_routes.py            # Login, Register, Logout
│   ├── main_routes.py            # Dashboard, Home, Profile
│   ├── resume_routes.py          # Resume upload + ATS scoring
│   ├── prediction_routes.py      # ML prediction + company match
│   ├── admin_routes.py           # Admin panel + analytics API
│   └── chatbot_routes.py         # PlaceBot AI chatbot
│
├── utils/
│   ├── ats_scorer.py             # ATS scoring engine
│   ├── resume_parser.py          # NLP resume parsing (PDF/DOC)
│   ├── skill_gap.py              # Skill gap analyzer + company DB
│   ├── predictor.py              # ML prediction engine
│   └── db_seeder.py              # Admin account seeder
│
├── templates/
│   ├── base.html                 # Base layout
│   ├── index.html                # Landing page
│   ├── dashboard.html            # Student dashboard
│   ├── profile.html              # User profile
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── resume/
│   │   ├── upload.html
│   │   └── result.html
│   ├── prediction/
│   │   └── result.html
│   ├── chatbot/
│   │   └── chat.html
│   └── admin/
│       ├── dashboard.html
│       └── user_detail.html
│
├── static/
│   ├── css/style.css
│   └── js/main.js
│
└── uploads/                      # Resume files stored here
```

---

## 🚀 Setup Instructions

### Step 1: Clone / Download the project
```bash
cd PlacePredictPro
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Step 4: Setup MySQL Database
```sql
mysql -u root -p < database_setup.sql
```

### Step 5: Create `.env` File
Create a `.env` file in the root directory:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost/mce_placement_db
ANTHROPIC_API_KEY=your-anthropic-api-key  # For PlaceBot chatbot
```

### Step 6: Train ML Models (Run Once)
```bash
python models/train_model.py
```
This generates `models/saved/` with trained Random Forest, XGBoost, ANN models.

### Step 7: Run the Application
```bash
python app.py
```
Open browser: **http://localhost:5000**

---

## 🔑 Default Admin Credentials
```
Email:    admin@mce.ac.in
Password: Admin@MCE2024
```
> ⚠️ Change this immediately in production!

---

## 🧠 ML Architecture

| Model | Algorithm | Purpose |
|-------|-----------|---------|
| Model 1 | Random Forest (GridSearchCV) | Placement Classification |
| Model 2 | XGBoost (GridSearchCV) | Placement Classification |
| Model 3 | ANN (3-layer, TensorFlow) | Placement Classification |
| Final | Ensemble (35:40:25 weighted) | Final Probability |

**Training Dataset:** 3,000 synthetic student records with realistic distributions  
**Features:** CGPA, 10th/12th %, Backlogs, Internships, Projects, Certifications, Communication, Coding, Aptitude, Technical, Extracurricular, ATS Score  
**Class Imbalance Handling:** SMOTE (Synthetic Minority Oversampling)

---

## 📊 Power BI Integration

To connect Power BI to the MySQL database:
1. Open Power BI Desktop
2. Get Data → MySQL Database
3. Server: `localhost`, Database: `mce_placement_db`
4. Import tables: `users`, `predictions`, `ats_scores`, `skill_gaps`
5. Create dashboards for:
   - ATS Score Distribution (histogram)
   - Placement Probability Trends (line chart)
   - Branch-wise Analysis (bar chart)
   - Most Common Missing Skills (word cloud)

---

## 🤖 PlaceBot AI Setup

PlaceBot uses the **Claude API (Anthropic)**. To enable it:
1. Get API key from https://console.anthropic.com
2. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`
3. PlaceBot works in fallback mode without the key (rule-based responses)

---

## 🌐 Deployment (Production)

### Using Gunicorn + Nginx:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

### Environment variables for production:
```
FLASK_ENV=production
SECRET_KEY=<strong-random-key>
DATABASE_URL=mysql+pymysql://user:pass@host/mce_placement_db
```

---

## 👥 Developed By
**MCE CSE (AI) Department Final Year Project Team**  
Motihari College of Engineering, Motihari, Bihar — 845401  
Training & Placement Cell

---

## 📄 License
This project is developed for academic purposes at MCE Motihari.
