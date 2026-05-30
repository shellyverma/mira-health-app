# MIRA – Medical Intelligence Robotic Automation

A health prediction web application built for Task 1 of the Junior AI/ML Developer assessment.

## Tech Stack
| Layer | Technology | Reason |
|-------|-----------|--------|
| Backend | Python + Flask | Lightweight, clean REST routing |
| Frontend | HTML + CSS + Bootstrap 5 | Simple, responsive, professional |
| Database | SQLite | Zero-config persistent storage |
| AI/ML API | Google Gemini 1.5 Flash | Free API, excellent medical reasoning |

## Features
- CRUD — Create, Read, Update, Delete patient records
- AI health prediction via Gemini AI on every save/update
- Input validation (email, DOB, positive numeric blood values)
- Color-coded blood value indicators (normal / warning / high)
- Full remarks view modal per patient
- Live search/filter across all records
- Rule-based fallback if API is unavailable

## Quick Start

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/mira-health-app.git
cd mira-health-app

# 2. Virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install
pip install -r requirements.txt

# 4. API Key — create .env file
copy .env.example .env
# Open .env → paste your Gemini API key
# Free key at: https://aistudio.google.com/app/apikey

# 5. Run
python app.py
# Open: http://127.0.0.1:5000
```

## Project Structure
```
mira-health-app/
├── app.py              # Flask app — all routes (CRUD + detail JSON)
├── database.py         # SQLite — all DB operations
├── ai_service.py       # Gemini AI integration + fallback logic
├── requirements.txt
├── .env.example        # API key template (safe to commit)
├── .gitignore          # Hides .env and mira.db
├── templates/
│   ├── index.html      # Patient list + search + detail modal
│   ├── add.html        # Add patient form
│   └── edit.html       # Edit patient form
└── static/css/
    └── style.css       # All custom styles
```

## Blood Value Reference Ranges
| Parameter | Normal | Warning | High Risk |
|-----------|--------|---------|-----------|
| Glucose | 70–99 mg/dL | 100–126 | >126 |
| Haemoglobin | 12–17.5 g/dL | — | <12 |
| Cholesterol | <200 mg/dL | 200–240 | >240 |
