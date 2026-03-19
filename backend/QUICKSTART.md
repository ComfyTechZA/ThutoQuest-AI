# Quick Start Guide - ThutoQuest AI Backend

## 🚀 5-Minute Setup

### 1. Clone & Navigate
```bash
cd ThutoQuest-AI/backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
# Edit .env with your OpenAI API key (optional for mock demo)
```

### 5. Run Tests (Verify Setup)
```bash
pytest tests/ -v
```

### 6. Start Server
```bash
python src/main.py
```

### 7. Test API

**Career Prediction**:
```bash
curl -X POST "http://localhost:8000/api/v1/predict-career" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU001",
    "national_id": "050125TXXXX01",
    "age": 15,
    "grade": 10,
    "school": "Example High",
    "district": "Gauteng"
  }'
```

**Quest Generation**:
```bash
curl -X POST "http://localhost:8000/api/v1/generate-quest" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU001",
    "national_id": "050125TXXXX01",
    "age": 15,
    "grade": 10,
    "school": "Example High",
    "district": "Gauteng"
  }'
```

### 8. View API Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📝 Common Commands

### Run Tests
```bash
# All tests
pytest tests/ -v

# Specific file
pytest tests/test_architecture.py -v

# Specific class
pytest tests/test_architecture.py::TestRandomForestCareerPredictor -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Only fast tests (skip slow)
pytest tests/ -m "not slow"
```

### Format Code
```bash
black src/
isort src/
```

### Type Checking
```bash
mypy src/ --ignore-missing-imports
```

### Lint Code
```bash
flake8 src/ --max-line-length=120
```

---

## 🔧 Project Structure

```
backend/
├── src/
│   ├── domain/          → Core business logic (framework-free)
│   ├── application/     → Use cases and DTOs
│   ├── infrastructure/  → ML models, databases, adapters
│   ├── interfaces/      → FastAPI routes and schemas
│   └── main.py         → Application entry point
├── tests/              → Test suite (40+ tests)
├── requirements.txt    → Dependencies
├── .env.example       → Configuration template
├── pytest.ini         → Test configuration
├── README.md          → User documentation
└── ARCHITECTURE.md    → Architecture details
```

---

## 🎯 What Works Out-of-Box

✅ Career prediction with 11 career paths  
✅ Quest generation with RAG integration  
✅ 40+ unit and integration tests (100% pass)  
✅ Comprehensive error handling  
✅ Pydantic validation  
✅ Mock data for development  
✅ Full API documentation  

---

## 📚 Layers Explained

| Layer | Purpose | Example |
|-------|---------|---------|
| **Domain** | Business logic | `CareerPrediction`, `RandomForestCareerPredictor` |
| **Application** | Use cases | `PredictCareerUseCase` orchestrates services |
| **Infrastructure** | Implementations | `InMemoryRepository`, ML models, Vector DB |
| **Interface** | HTTP API | FastAPI routes, Pydantic schemas |

---

## 🤖 ML Models

### Career Prediction
- **Algorithm**: Random Forest Classifier
- **Features**: 13 years of mastery data (15 features)
- **Output**: Career path + confidence (0-1)
- **Careers**: 11 different paths

### Quest Generation  
- **Method**: LangChain + RAG
- **Sources**: DBE textbook vector database
- **Content**: Math problems, coding challenges
- **Output**: Personalized quest with difficulty level

---

## 🐛 Troubleshooting

### Import Errors
```python
# Add backend to Python path
export PYTHONPATH="${PYTHONPATH}:./backend"
```

### Database Errors
```python
# Currently using in-memory (no DB needed)
# For PostgreSQL: update DATABASE_URL in .env
```

### OpenAI API Errors
```python
# OpenAI is optional for basic demo
# Add OPENAI_API_KEY to .env to enable LLM features
```

---

## 📞 Support

- Refer to `README.md` for full documentation
- Check `ARCHITECTURE.md` for design details
- Run tests: `pytest tests/ -v`
- View API docs: http://localhost:8000/docs

---

**Happy Coding! 🚀**
