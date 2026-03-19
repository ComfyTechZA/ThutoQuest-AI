"""
Application Layer: Use Cases and Application Services
Orchestrates domain services and repositories
"""

from typing import Optional
from dataclasses import dataclass
import logging

from src.domain.models import (
    StudentProfile,
    StudentMasteryHistory,
    CareerPrediction,
    Quest,
    StudentMasteryRepository,
    CareerPredictionService,
    QuestGenerationService,
    StudentNotFoundError,
    InvalidMasteryDataError,
)

logger = logging.getLogger(__name__)


# ============================================================================
# DTOs (Data Transfer Objects)
# ============================================================================

@dataclass
class PredictCareerRequest:
    """Request DTO for career prediction"""
    student_id: str
    national_id: str
    age: int
    grade: int
    school: str
    district: str
    
    def to_domain(self) -> StudentProfile:
        """Convert DTO to domain model"""
        return StudentProfile(
            student_id=self.student_id,
            national_id=self.national_id,
            age=self.age,
            grade=self.grade,
            school=self.school,
            district=self.district
        )


@dataclass
class PredictCareerResponse:
    """Response DTO for career prediction"""
    prediction_id: str
    student_id: str
    primary_career: str
    confidence: float
    alternative_careers: list
    reasoning: dict
    
    @staticmethod
    def from_domain(prediction: CareerPrediction) -> "PredictCareerResponse":
        """Convert domain model to DTO"""
        return PredictCareerResponse(
            prediction_id=prediction.prediction_id,
            student_id=prediction.student_id,
            primary_career=prediction.primary_career.value,
            confidence=round(prediction.confidence, 2),
            alternative_careers=[
                {"path": c.value, "confidence": round(conf, 2)}
                for c, conf in prediction.alternative_careers
            ],
            reasoning=prediction.reasoning
        )


@dataclass
class GenerateQuestRequest:
    """Request DTO for quest generation"""
    student_id: str
    national_id: str
    age: int
    grade: int
    school: str
    district: str


@dataclass
class GenerateQuestResponse:
    """Response DTO for quest generation"""
    quest_id: str
    title: str
    description: str
    content: str
    difficulty: str
    quest_type: str
    subject: str
    topics: list
    estimated_time_minutes: int
    points_reward: int
    hint: Optional[str]
    
    @staticmethod
    def from_domain(quest: Quest) -> "GenerateQuestResponse":
        """Convert domain model to DTO"""
        return GenerateQuestResponse(
            quest_id=quest.quest_id,
            title=quest.title,
            description=quest.description,
            content=quest.content,
            difficulty=quest.difficulty.value,
            quest_type=quest.quest_type.value,
            subject=quest.subject,
            topics=quest.topics,
            estimated_time_minutes=quest.estimated_time_minutes,
            points_reward=quest.points_reward,
            hint=quest.solution_hint
        )


# ============================================================================
# USE CASES
# ============================================================================

class PredictCareerUseCase:
    """
    Use case: Predict career path for student.
    Orchestrates mastery retrieval and prediction service.
    """
    
    def __init__(
        self,
        mastery_repository: StudentMasteryRepository,
        prediction_service: CareerPredictionService
    ):
        """Initialize use case with dependencies"""
        self.mastery_repo = mastery_repository
        self.prediction_service = prediction_service
    
    async def execute(
        self,
        request: PredictCareerRequest
    ) -> PredictCareerResponse:
        """
        Execute career prediction.
        
        Args:
            request: Career prediction request
            
        Returns:
            Career prediction response
            
        Raises:
            StudentNotFoundError: If student not found
            InvalidMasteryDataError: If mastery data invalid
        """
        # Convert request to domain model
        student_profile = request.to_domain()
        
        # Validate student profile
        if not student_profile.validate():
            raise InvalidMasteryDataError("Invalid student profile data")
        
        # Retrieve mastery history
        mastery_history = await self.mastery_repo.get_mastery_history(
            request.student_id
        )
        
        if not mastery_history:
            raise StudentNotFoundError(f"Student {request.student_id} not found")
        
        # Execute prediction
        prediction = await self.prediction_service.predict(
            student_profile=student_profile,
            mastery_history=mastery_history
        )
        
        # Save prediction
        await self.mastery_repo.save_prediction(prediction)
        
        # Convert to response DTO
        response = PredictCareerResponse.from_domain(prediction)
        
        logger.info(f"Career prediction completed for {request.student_id}")
        return response


class GenerateQuestUseCase:
    """
    Use case: Generate personalized quest for student.
    Orchestrates mastery retrieval, career prediction, and quest generation.
    """
    
    def __init__(
        self,
        mastery_repository: StudentMasteryRepository,
        prediction_service: CareerPredictionService,
        quest_service: QuestGenerationService
    ):
        """Initialize use case with dependencies"""
        self.mastery_repo = mastery_repository
        self.prediction_service = prediction_service
        self.quest_service = quest_service
    
    async def execute(
        self,
        request: GenerateQuestRequest
    ) -> GenerateQuestResponse:
        """
        Generate personalized quest for student.
        
        Args:
            request: Quest generation request
            
        Returns:
            Generated quest response
            
        Raises:
            StudentNotFoundError: If student not found
            InvalidMasteryDataError: If mastery data invalid
        """
        # Create student profile
        student_profile = StudentProfile(
            student_id=request.student_id,
            national_id=request.national_id,
            age=request.age,
            grade=request.grade,
            school=request.school,
            district=request.district
        )
        
        # Validate
        if not student_profile.validate():
            raise InvalidMasteryDataError("Invalid student profile data")
        
        # Retrieve mastery history
        mastery_history = await self.mastery_repo.get_mastery_history(
            request.student_id
        )
        
        if not mastery_history:
            raise StudentNotFoundError(f"Student {request.student_id} not found")
        
        # Get career prediction for context (optional)
        try:
            career_prediction = await self.prediction_service.predict(
                student_profile=student_profile,
                mastery_history=mastery_history
            )
        except Exception as e:
            logger.warning(f"Could not get career prediction: {str(e)}")
            career_prediction = None
        
        # Generate quest
        quest = await self.quest_service.generate_quest(
            student_id=request.student_id,
            student_profile=student_profile,
            mastery_history=mastery_history,
            career_prediction=career_prediction
        )
        
        # Save quest
        await self.mastery_repo.save_quest(quest)
        
        # Convert to response DTO
        response = GenerateQuestResponse.from_domain(quest)
        
        logger.info(f"Quest generation completed for {request.student_id}")
        return response


class HealthCheckUseCase:
    """Use case: System health check"""
    
    async def execute(self) -> dict:
        """Execute health check"""
        return {
            "status": "healthy",
            "service": "ThutoQuest Career & Quest Backend",
            "version": "1.0.0"
        }
