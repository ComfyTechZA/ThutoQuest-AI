# Clean Hexagonal Architecture - Detailed Documentation

## 📐 Architecture Overview

ThutoQuest AI Backend implements **Clean Hexagonal Architecture** (also known as Ports and Adapters pattern), which ensures:

- ✅ **Framework Independence**: Business logic doesn't depend on frameworks
- ✅ **Testability**: Easy to unit test without external dependencies
- ✅ **Scalability**: Easy to swap implementations (e.g., database, ML models)
- ✅ **Maintainability**: Clear separation of concerns

---

## 🔄 Architecture Diagram

```
                    ┌─────────────────────────────────┐
                    │    HTTP Clients / External APIs │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │     Interface Layer             │
                    │  (FastAPI Routes, Pydantic)     │
                    │  ✓ predict-career endpoint      │
                    │  ✓ generate-quest endpoint      │
                    │  ✓ Error handling & validation  │
                    └──────────────┬──────────────────┘
                                   │
    ┌──────────────────────────────┼──────────────────────────────┐
    │                              │                              │
    │   ┌────────────────────┐ ┌────────────────────────────────┐ │
    │   │ Application Layer  │ │  Application Layer             │ │
    │   │ (Use Cases)        │ │  (Use Cases continued)         │ │
    │   │                    │ │                                │ │
    │   │ Use Cases:         │ │  ✓ Dependency Injection       │ │
    │   │ ✓ PredictionUC     │ │  ✓ Request/Response DTOs      │ │
    │   │ ✓ QuestUC         │ │  ✓ Orchestration              │ │
    │   └────────┬───────────┘ └──────────┬─────────────────────┘ │
    │            │                        │                        │
    │   ┌────────▼──────────────────────────────────┐              │
    │   │   Domain Layer (CORE - Framework Free)    │              │
    │   │                                            │              │
    │   │  Entities:                                │              │
    │   │  ✓ StudentProfile, StudentMasteryHistory  │              │
    │   │  ✓ CareerPrediction, Quest                │              │
    │   │                                            │              │
    │   │  Domain Services (Abstract):              │              │
    │   │  ✓ CareerPredictionService                │              │
    │   │  ✓ QuestGenerationService                 │              │
    │   │                                            │              │
    │   │  Ports (Abstract Interfaces):             │              │
    │   │  ✓ StudentMasteryRepository                │              │
    │   │  ✓ VectorDatabasePort                      │              │
    │   │                                            │              │
    │   │  Business Logic:                          │              │
    │   │  ✓ Career profile matching                │              │
    │   │  ✓ Quest difficulty calculation           │              │
    │   │  ✓ Validation rules                       │              │
    │   └────┬────────────────────────────────────┬─┘              │
    │        │                                    │                │
    │   ┌────▼──────────┐         ┌──────────────▼──────┐          │
    │   │Infrastructure │         │ Infrastructure      │          │
    │   │Adapter 1      │         │ Adapter 2           │          │
    │   │               │         │                     │          │
    │   │ RandomForest  │         │ Repository          │          │
    │   │ Predictor     │         │ (PostgreSQL)        │          │
    │   │ (Impl)        │         │ (Impl)              │          │
    │   └────┬──────────┘         └──────┬──────────────┘          │
    │   ┌────┴──────────┐         ┌──────┴──────────────┐          │
    │   │ scikit-learn  │         │ SQLAlchemy ORM     │          │
    │   │ ML Framework  │         │ PostgreSQL Driver  │          │
    │   └───────────────┘         └────────────────────┘          │
    │                                                              │
    │   ┌──────────────────────────────────────────────────────┐  │
    │   │  Infrastructure Layer - Other Adapters              │  │
    │   │                                                      │  │
    │   │  LangChain RAG Generator                            │  │
    │   │  ✓ Implements QuestGenerationService               │  │
    │   │  ✓ Uses DBETextbookVectorDB                         │  │
    │   │  ✓ LangChain + OpenAI integration                   │  │
    │   │                                                      │  │
    │   │  Vector Database Adapter                           │  │
    │   │  ✓ Implements VectorDatabasePort                    │  │
    │   │  ✓ Abstract - can use Chroma/Pinecone/Weaviate     │  │
    │   │                                                      │  │
    │   │  Repository Adapters                               │  │
    │   │  ✓ InMemoryRepository (dev/testing)                │  │
    │   │  ✓ PostgreSQLRepository (production)               │  │
    │   └──────────────────────────────────────────────────────┘  │
    │                                                              │
    └──────────────────────────────────────────────────────────────┘
```

---

## 📁 Directory Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py                          # FastAPI app entry point
│   │
│   ├── domain/                          # 🎯 CORE BUSINESS LOGIC
│   │   ├── __init__.py
│   │   └── models.py                    # Entities, ports, services, exceptions
│   │       ├── Enums: CareerPath, QuestDifficulty, etc.
│   │       ├── Value Objects: StudentProfile, MasteryScore
│   │       ├── Entities: CareerPrediction, Quest
│   │       ├── Abstract Services: CareerPredictionService
│   │       ├── Abstract Ports: StudentMasteryRepository
│   │       └── Domain Exceptions
│   │
│   ├── application/                     # 🔄 ORCHESTRATION LAYER
│   │   ├── __init__.py
│   │   └── use_cases.py                 # Use cases & DTOs
│   │       ├── DTOs: PredictCareerRequest/Response
│   │       ├── Use Cases: PredictCareerUseCase, GenerateQuestUseCase
│   │       └── HealthCheckUseCase
│   │
│   ├── infrastructure/                  # 🔧 IMPLEMENTATIONS & ADAPTERS
│   │   ├── __init__.py
│   │   ├── ml_models.py                 # RandomForestCareerPredictor
│   │   ├── rag_quest_generator.py       # LangChain RAG + VectorDB
│   │   └── repositories.py              # InMemory & PostgreSQL repos
│   │
│   └── interfaces/                      # 🌐 HTTP INTERFACE
│       ├── __init__.py
│       └── api.py                       # FastAPI routes, Pydantic schemas
│           ├── Pydantic Schemas (Request/Response)
│           ├── Error Response Schemas
│           ├── Dependency Injection
│           └── API Endpoints
│
├── tests/                               # ✅ TESTS
│   ├── __init__.py
│   └── test_architecture.py             # 40+ unit + integration tests
│       ├── Domain Model Tests
│       ├── ML Model Tests
│       ├── Repository Tests
│       ├── Use Case Tests
│       └── Integration Tests
│
├── requirements.txt                     # Dependencies
├── .env.example                         # Environment config template
├── README.md                            # User documentation
└── ARCHITECTURE.md                      # This file
```

---

## 🎯 Layer Responsibilities

### 1. Domain Layer

**Purpose**: Pure business logic, framework-agnostic

**Contains**:
- **Entities**: `StudentProfile`, `CareerPrediction`, `Quest`
- **Value Objects**: `StudentMasteryHistory`, `MasteryScore`
- **Domain Services** (Abstract): Define what services do
- **Ports** (Abstract Interfaces): Define external dependencies
- **Domain Exceptions**: Business-specific errors
- **Enums**: `CareerPath`, `QuestDifficulty`, etc.

**Key Principle**: NO IMPORTS from other layers (except domain)

**Example**:
```python
# domain/models.py - Pure business logic
class CareerPrediction:
    def is_high_confidence(self, threshold: float = 0.7) -> bool:
        return self.confidence >= threshold

class CareerPredictionService(ABC):
    @abstractmethod
    async def predict(self, profile: StudentProfile) -> CareerPrediction:
        pass
```

**Benefits**:
- ✅ Testable without frameworks
- ✅ Framework changes don't affect logic
- ✅ Clear business rules
- ✅ Reusable across projects

---

### 2. Application Layer

**Purpose**: Orchestrates domain services and repositories

**Contains**:
- **Use Cases**: `PredictCareerUseCase`, `GenerateQuestUseCase`
- **DTOs**: Data Transfer Objects for requests/responses
- **Application Services**: Coordinate use case execution

**Key Principle**: Depends on domain layer ONLY

**Example**:
```python
# application/use_cases.py
class PredictCareerUseCase:
    def __init__(self, repository: StudentMasteryRepository, 
                 service: CareerPredictionService):
        self.repository = repository
        self.service = service
    
    async def execute(self, request: PredictCareerRequest):
        history = await self.repository.get_mastery_history(...)
        prediction = await self.service.predict(...)
        await self.repository.save_prediction(prediction)
        return response_dto
```

**Benefits**:
- ✅ Centralizes business workflows
- ✅ Translation between external and domain models
- ✅ Transaction management
- ✅ Easy to test with mocks

---

### 3. Infrastructure Layer

**Purpose**: Implements abstract ports and integrates external systems

**Contains**:
- **ML Models**: `RandomForestCareerPredictor` (implements abstract service)
- **Vector Database**: `DBETextbookVectorDB` (implements abstract port)
- **RAG Generator**: `LangChainRAGQuestGenerator` (implements abstract service)
- **Repositories**: `InMemoryMasteryRepository`, `PostgreSQLMasteryRepository`

**Key Principle**: Implements domain ports, depends on frameworks/libraries

**Example**:
```python
# infrastructure/ml_models.py
class RandomForestCareerPredictor(CareerPredictionService):
    """Concrete implementation of domain service"""
    
    def __init__(self):
        self.model = RandomForestClassifier(...)  # ML framework dependency
    
    async def predict(self, profile, history) -> CareerPrediction:
        # Implementation using scikit-learn
        features = self._prepare_features(profile, history)
        career = self.model.predict(features)
        return CareerPrediction(...)
```

**Benefits**:
- ✅ Easy to swap implementations (e.g., ML model)
- ✅ Decouples business logic from external systems
- ✅ Multiple implementations can coexist
- ✅ Testing: use InMemory in tests, PostgreSQL in prod

---

### 4. Interface Layer

**Purpose**: Exposes API via HTTP, handles HTTP details

**Contains**:
- **FastAPI Routes**: Endpoints for predictions and quests
- **Pydantic Schemas**: Request/response validation
- **Error Handlers**: HTTP error handling
- **Dependency Injection**: FastAPI dependency resolution

**Key Principle**: Thin layer, depends on application layer

**Example**:
```python
# interfaces/api.py
@app.post("/predict-career")
async def predict_career(
    request: PredictCareerRequestSchema,
    use_case = Depends(get_predict_career_use_case)
) -> PredictCareerResponseSchema:
    result = await use_case.execute(request)
    return PredictCareerResponseSchema.from_domain(result)
```

**Benefits**:
- ✅ Thin HTTP adapter
- ✅ Easy to add more interfaces (gRPC, CLI, etc.)
- ✅ Request/response validation
- ✅ Clear error handling

---

## 🔌 Ports and Adapters Pattern

### What are Ports and Adapters?

- **Ports** (Abstract Interfaces): Define what external systems should do
- **Adapters** (Concrete Implementations): Implement ports for specific technologies

### Example: StudentMasteryRepository

**Port** (Domain - defines contract):
```python
# domain/models.py
class StudentMasteryRepository(ABC):
    @abstractmethod
    async def get_mastery_history(self, student_id) -> StudentMasteryHistory:
        pass
```

**Adapter 1** (In-Memory - for development):
```python
# infrastructure/repositories.py
class InMemoryMasteryRepository(StudentMasteryRepository):
    def __init__(self):
        self.storage = {}
    
    async def get_mastery_history(self, student_id):
        return self.storage.get(student_id)
```

**Adapter 2** (PostgreSQL - for production):
```python
# infrastructure/repositories.py
class PostgreSQLMasteryRepository(StudentMasteryRepository):
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
    
    async def get_mastery_history(self, student_id):
        # Query from PostgreSQL
        return session.query(StudentMastery).filter(...).first()
```

**Benefit**: Swap implementations without changing domain logic!

---

## 📊 Data Flow Example: Career Prediction

```
HTTP Request (FastAPI)
         ↓
PredictCareerRequestSchema (Pydantic validation)
         ↓
Dependency Injection (get_predict_career_use_case)
         ↓
PredictCareerUseCase.execute()
         │
         ├─→ StudentMasteryRepository.get_mastery_history() [Abstract]
         │   └─→ InMemoryMasteryRepository [Concrete]
         │       └─→ Loads mock data
         │
         ├─→ CareerPredictionService.predict() [Abstract]
         │   └─→ RandomForestCareerPredictor [Concrete]
         │       ├─→ scikit-learn RandomForest
         │       └─→ Returns CareerPrediction
         │
         └─→ StudentMasteryRepository.save_prediction() [Abstract]
             └─→ InMemoryMasteryRepository [Concrete]
                 └─→ Stores in memory
         ↓
CareerPrediction (Domain Entity)
         ↓
PredictCareerResponse (DTO)
         ↓
PredictCareerResponseSchema (Pydantic)
         ↓
HTTP Response (JSON)
```

---

## ✅ Testing Strategy

### By Layer

**Domain Tests** (Pure Logic - No Framework)
```python
def test_career_prediction_is_high_confidence():
    prediction = CareerPrediction(..., confidence=0.85)
    assert prediction.is_high_confidence() is True
```

**Application Tests** (Orchestration - Mock Dependencies)
```python
async def test_predict_career_use_case():
    mock_repo = MagicMock()
    mock_service = MagicMock()
    use_case = PredictCareerUseCase(mock_repo, mock_service)
    result = await use_case.execute(request)
    assert result is not None
```

**Infrastructure Tests** (Adapter-Specific)
```python
async def test_random_forest_predicts_career():
    predictor = RandomForestCareerPredictor()
    result = await predictor.predict(profile, history)
    assert isinstance(result, CareerPrediction)
```

**Integration Tests** (Full Pipeline)
```python
async def test_full_prediction_pipeline():
    # All layers working together
    result = await use_case.execute(request)
    assert result.prediction_id is not None
```

---

## 🔄 Dependency Injection

### Pattern: Constructor Injection

Application layer receives dependencies via constructor:

```python
# application/use_cases.py
class PredictCareerUseCase:
    def __init__(
        self,
        repository: StudentMasteryRepository,  # Port 1
        service: CareerPredictionService       # Port 2
    ):
        self.repository = repository
        self.service = service
```

### FastAPI DI

Interface layer uses FastAPI dependencies:

```python
# interfaces/api.py
async def get_predict_career_use_case():
    repository = InMemoryMasteryRepository()
    predictor = RandomForestCareerPredictor()
    return PredictCareerUseCase(repository, predictor)

@app.post("/predict-career")
async def predict_career(
    request: PredictCareerRequestSchema,
    use_case = Depends(get_predict_career_use_case)  # Injected
):
    return await use_case.execute(request)
```

**Benefits**:
- ✅ Easy to mock in tests
- ✅ Flexible configuration per environment
- ✅ Clear dependency declaration
- ✅ Single responsibility

---

## 🚀 Scaling & Evolution

### Adding a New ML Model

1. **Create domain port** (if needed):
   ```python
   # domain/models.py
   class AlternativePredictionService(ABC):
       async def predict(...) -> CareerPrediction:
           pass
   ```

2. **Implement in infrastructure**:
   ```python
   # infrastructure/ml_models.py
   class GPTBasedPredictor(AlternativePredictionService):
       async def predict(...):
           # Implementation
   ```

3. **Use in application**:
   ```python
   # interfaces/api.py - add endpoint or decorator to switch
   from config import get_ml_model
   
   use_case = PredictCareerUseCase(
       repo,
       get_ml_model("random_forest")  # or "gpt_based"
   )
   ```

### Adding a New Database

1. **Implement existing port**:
   ```python
   # infrastructure/repositories.py
   class MongoDBMasteryRepository(StudentMasteryRepository):
       async def get_mastery_history(...):
           # Query MongoDB
   ```

2. **Switch in DI**:
   ```python
   async def get_mastery_repository():
       if os.getenv("DB_TYPE") == "postgresql":
           return PostgreSQLMasteryRepository(...)
       else:
           return MongoDBMasteryRepository(...)
   ```

---

## ✨ Key Advantages

| Aspect | Benefit |
|--------|---------|
| **Testability** | Each layer testable independently with mocks |
| **Maintainability** | Clear separation, changes don't cascade |
| **Flexibility** | Swap implementations without affecting logic |
| **Scalability** | Easy to add features and layers |
| **Documentation** | Architecture is self-documenting via ports |
| **Team** | Clear responsibilities per layer |
| **Framework** | Upgrade/change FastAPI without touching business logic |
| **Reuse** | Domain logic usable across different interfaces (HTTP, gRPC, CLI) |

---

## 📚 Further Reading

- [Alistair Cockburn - Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Uncle Bob - Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Clean Code in Python](https://www.oreilly.com/library/view/clean-code-in/9781788835831/)

---

**Version**: 1.0.0  
**Last Updated**: March 20, 2026  
**Architecture Pattern**: Clean Hexagonal Architecture (Ports & Adapters)
