# 🎓 ThutoQuest-AI Tournament Build - Quick Start

## 🚀 What You Get

A **single-file FastAPI application** (`tournament_build.py`) that demonstrates your entire platform in one window during a 5-minute pitch:

### ✅ Features Included
- **📝 Student Authentication** - Socratic AI Tutor login system
- **🧠 Socratic AI Tutor** - RAG-powered contextual questioning
- **🎵 Amapiano Music Mnemonics** - South African rhythm-based memory aids  
- **🤖 Career Prediction ML** - Random Forest classifier analyzing 13 years of mastery data
- **📊 Single-Page Dashboard** - Embedded Tailwind CSS UI (no window switching)
- **🎪 /demo Endpoint** - Sequential automation for live demonstrations

---

## 📋 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_tournament.txt
```

### 2. Run the Server
```bash
python tournament_build.py
```

Output:
```
╔═══════════════════════════════════════════════════════════════════╗
║          🎓 ThutoQuest-AI Tournament Build                        ║
║          Single-File FastAPI Demo for 5-Minute Pitch             ║
╚═══════════════════════════════════════════════════════════════════╝

🚀 Starting server on http://localhost:8000
📊 Dashboard: http://localhost:8000/
🔌 API Docs: http://localhost:8000/docs
```

### 3. Open the Dashboard
Visit: **http://localhost:8000/**

---

## 🎪 Live Demo Walkthrough

### Option A: Click "Run Complete Demo" Button
1. Opens dashboard at `http://localhost:8000/`
2. Click blue **"▶️ Run Complete Demo"** button
3. Watch all 4 steps execute sequentially:
   - ✅ Step 1: Student Authentication (2 sec)
   - ✅ Step 2: Socratic AI Tutor (2 sec)
   - ✅ Step 3: Amapiano Mnemonic (2 sec)
   - ✅ Step 4: Career Prediction (2 sec)
4. Total execution: **~10 seconds** with beautiful result cards

### Option B: cURL / API Direct
```bash
# Run demo endpoint
curl -X POST http://localhost:8000/demo

# Check system status
curl http://localhost:8000/demo/status
```

### Response Example
```json
{
  "timestamp": "2024-03-20T10:30:45.123456",
  "student": {
    "student_id": "uuid-...",
    "name": "Thabo Kimani",
    "grade": 10,
    "school": "Soweto Central High",
    "mastery_score": 0.82
  },
  "socratic_question": {
    "question": "When using the quadratic formula, why do we need a, b, and c?",
    "difficulty": "intermediate",
    "topic": "Quadratic Equations",
    "hint": "Formula components"
  },
  "amapiano_mnemonic": {
    "topic": "Quadratic Formula",
    "mnemonic": "ABCD: All Brackets Come Down...",
    "rhythm_pattern": "🥁 Boom-Chick-Boom-Tap...",
    "lyric": "Ay-ee, formula don't lie...",
    "beat_tempo": 110
  },
  "career_prediction": {
    "recommended_path": "data_scientist",
    "confidence": 0.87,
    "alternative_paths": ["software_engineer", "mathematician"],
    "strengths": ["Math", "Language"],
    "improvement_areas": []
  },
  "total_duration_seconds": 8.45
}
```

---

## 🔐 Test Credentials

```
Email:       test.student@thutoquest.edu.za
Password:    TestPassword123!
National ID: GH123456789012
Student:     Thabo Kimani (Grade 10)
```

---

## 📊 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Single-page Tailwind dashboard |
| `/demo` | POST | Run complete sequential demo |
| `/demo/status` | GET | System status & feature availability |
| `/login` | POST | Manual student authentication |
| `/health` | GET | Health check |
| `/api/info` | GET | Platform information & endpoints |
| `/docs` | GET | FastAPI Swagger UI documentation |

---

## 🎯 Architecture Inside the Single File

### Imported from Your Project:
✅ **Domain Models** (`backend/src/domain/models.py`)
- `StudentProfile`, `CareerPath`, `QuestDifficulty`
- Mastery tracking data structures

✅ **ML Models** (`backend/src/infrastructure/ml_models.py`)
- `RandomForestCareerPredictor` - analyzes 13 years of mastery data
- Career profile matching (11 career paths)
- Feature extraction from student performance

✅ **Database Schema** (`database/schema.sql`)
- Student records, curriculum nodes, mastery tracking
- Used as reference for data models

### Custom Components for Demo:
✨ **Socratic AI Tutor** - RAG-powered question generation
✨ **Amapiano Mnemonic Generator** - Music-based learning aids
✨ **Authentication Service** - Session token management
✨ **Tailwind Dashboard** - Embedded 1500-line HTML/CSS/JS

---

## 🎬 Perfect for Your 5-Minute Pitch

**Timeline:**
- 0:00 - Show dashboard at `http://localhost:8000/`
- 0:15 - Click "Run Complete Demo"
- 0:45 - Results populate **live** on one page
- 1:00 - Walk through each component:
  - Student profile (15 sec)
  - Socratic question (20 sec)
  - Amapiano mnemonic (20 sec)
  - Career prediction (20 sec)
- 2:15 - Show API docs at `/docs` if time permits
- 3:00 - Q&A + technical deep-dive demo by running again

**Advantages:**
✅ No window switching
✅ Beautiful Tailwind UI
✅ Real data flows
✅ Live ML prediction
✅ Professional presentation
✅ Single file = easy to run anywhere

---

## 🛠 Customization

Edit `tournament_build.py` to:
- Add more career paths in `CAREER_PROFILES`
- Extend Socratic questions in `KNOWLEDGE_BASE`
- Add more Amapiano mnemonics
- Modify test student data
- Customize dashboard colors/layout

---

## 📝 Notes for Judges

The demo showcases:
1. **Full Stack Integration** - Backend logic + ML + Frontend in one deployment
2. **Smart AI** - Socratic tutoring + Career prediction
3. **Cultural Relevance** - Amapiano rhythms for South African context
4. **Offline-Ready** - All logic runs locally, no external API calls
5. **Production-Grade** - FastAPI, Pydantic validation, proper error handling
6. **User Experience** - Smooth animations, responsive design, accessibility

---

## 🚀 Next Steps

1. **Run locally**: `python tournament_build.py`
2. **Open dashboard**: `http://localhost:8000/`
3. **Click demo button** and present the results
4. **Show API** at `/docs`
5. **Answer technical questions** using the live endpoint

Good luck with your pitch! 🎓✨
