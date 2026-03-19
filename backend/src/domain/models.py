"""
Domain Layer: Core Business Models and Entities
Represents the business logic independent of frameworks
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime
from abc import ABC, abstractmethod
import uuid


# ============================================================================
# DOMAIN ENUMS
# ============================================================================

class CareerPath(str, Enum):
    """Potential career paths based on student profile"""
    SOFTWARE_ENGINEER = "software_engineer"
    DATA_SCIENTIST = "data_scientist"
    MECHANICAL_ENGINEER = "mechanical_engineer"
    ELECTRICAL_ENGINEER = "electrical_engineer"
    CIVIL_ENGINEER = "civil_engineer"
    MATHEMATICIAN = "mathematician"
    PHYSICIST = "physicist"
    ACTUARIAL_SCIENTIST = "actuarial_scientist"
    PHARMACIST = "pharmacist"
    MEDICAL_DOCTOR = "medical_doctor"
    EDUCATOR = "educator"


class QuestDifficulty(str, Enum):
    """Quest difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class QuestType(str, Enum):
    """Types of quests"""
    MATH_PROBLEM = "math_problem"
    CODING_CHALLENGE = "coding_challenge"
    MULTI_STEP = "multi_step"
    PROJECT_BASED = "project_based"


# ============================================================================
# DOMAIN VALUE OBJECTS
# ============================================================================

@dataclass(frozen=True)
class StudentProfile:
    """Immutable student profile for prediction"""
    student_id: str
    national_id: str
    age: int
    grade: int
    school: str
    district: str
    
    def validate(self) -> bool:
        """Validate student profile data"""
        if not self.student_id or not self.national_id:
            return False
        if self.age < 5 or self.age > 30:
            return False
        if self.grade < 0 or self.grade > 12:
            return False
        return True


@dataclass(frozen=True)
class MasteryScore:
    """Immutable mastery score for a subject/topic"""
    subject: str
    topic: str
    score: float  # 0.0 to 1.0
    timestamp: datetime
    
    def __post_init__(self):
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(f"Mastery score must be 0.0-1.0, got {self.score}")


@dataclass(frozen=True)
class StudentMasteryHistory:
    """13-year mastery history for a student"""
    student_id: str
    grades: List[int]  # 0-12 (R-12 equivalent)
    math_scores: List[List[float]]  # Per grade, per topic
    science_scores: List[List[float]]  # Per grade, per topic
    language_scores: List[List[float]]  # Per grade, per topic
    consistency_score: float  # 0.0-1.0
    improvement_rate: float  # Slope of improvement
    
    def years_of_data(self) -> int:
        """Return number of years of data available"""
        return len(self.grades)


# ============================================================================
# DOMAIN ENTITIES
# ============================================================================

@dataclass
class CareerPrediction:
    """Domain entity: Career prediction result"""
    prediction_id: str
    student_id: str
    primary_career: CareerPath
    confidence: float  # 0.0-1.0
    alternative_careers: List[tuple]  # [(CareerPath, confidence), ...]
    reasoning: Dict[str, str]  # Feature importance explanations
    predicted_at: datetime
    
    def is_high_confidence(self, threshold: float = 0.7) -> bool:
        """Check if prediction is high confidence"""
        return self.confidence >= threshold
    
    def get_top_3_careers(self) -> List[tuple]:
        """Get top 3 career options"""
        top = [(self.primary_career, self.confidence)]
        top.extend(self.alternative_careers[:2])
        return top


@dataclass
class Quest:
    """Domain entity: Educational quest/challenge"""
    quest_id: str
    student_id: str
    title: str
    description: str
    content: str  # The actual problem/challenge
    difficulty: QuestDifficulty
    quest_type: QuestType
    subject: str
    topics: List[str]
    source_material: str  # Reference to DBE textbook
    estimated_time_minutes: int
    points_reward: int
    solution_hint: Optional[str]
    reference_grade: int
    generated_at: datetime
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation"""
        return {
            "quest_id": self.quest_id,
            "title": self.title,
            "description": self.description,
            "content": self.content,
            "difficulty": self.difficulty.value,
            "type": self.quest_type.value,
            "subject": self.subject,
            "topics": self.topics,
            "estimated_time": self.estimated_time_minutes,
            "points": self.points_reward,
            "hint": self.solution_hint
        }


# ============================================================================
# DOMAIN REPOSITORIES (Ports)
# ============================================================================

class StudentMasteryRepository(ABC):
    """Port: Repository for student mastery data"""
    
    @abstractmethod
    async def get_mastery_history(
        self, 
        student_id: str
    ) -> Optional[StudentMasteryHistory]:
        """Retrieve student's 13-year mastery history"""
        pass
    
    @abstractmethod
    async def save_prediction(
        self,
        prediction: CareerPrediction
    ) -> bool:
        """Save career prediction to storage"""
        pass


class QuestRepository(ABC):
    """Port: Repository for quest data"""
    
    @abstractmethod
    async def save_quest(self, quest: Quest) -> bool:
        """Save generated quest to storage"""
        pass
    
    @abstractmethod
    async def get_quests_by_student(
        self,
        student_id: str
    ) -> List[Quest]:
        """Retrieve quests assigned to student"""
        pass


class VectorDatabasePort(ABC):
    """Port: Abstract vector database interface"""
    
    @abstractmethod
    async def search_content(
        self,
        query: str,
        subject: str,
        grade: int,
        top_k: int = 5
    ) -> List[Dict]:
        """Search for relevant content from DBE textbooks"""
        pass


# ============================================================================
# DOMAIN SERVICES
# ============================================================================

class CareerPredictionService(ABC):
    """Domain service: Career prediction logic"""
    
    @abstractmethod
    async def predict(
        self,
        student_profile: StudentProfile,
        mastery_history: StudentMasteryHistory
    ) -> CareerPrediction:
        """Predict career path for student"""
        pass
    
    @abstractmethod
    def calculate_reasoning(
        self,
        feature_importance: Dict[str, float]
    ) -> Dict[str, str]:
        """Convert feature importance to human-readable reasoning"""
        pass


class QuestGenerationService(ABC):
    """Domain service: Quest generation logic"""
    
    @abstractmethod
    async def generate_quest(
        self,
        student_id: str,
        student_profile: StudentProfile,
        mastery_history: StudentMasteryHistory,
        career_prediction: Optional[CareerPrediction] = None
    ) -> Quest:
        """Generate a personalized quest for student"""
        pass


# ============================================================================
# DOMAIN EXCEPTIONS
# ============================================================================

class DomainException(Exception):
    """Base domain exception"""
    pass


class StudentNotFoundError(DomainException):
    """Student not found in system"""
    pass


class InvalidMasteryDataError(DomainException):
    """Invalid mastery data provided"""
    pass


class PredictionFailedError(DomainException):
    """Career prediction failed"""
    pass


class QuestGenerationError(DomainException):
    """Quest generation failed"""
    pass


class VectorDatabaseError(DomainException):
    """Vector database access failed"""
    pass
