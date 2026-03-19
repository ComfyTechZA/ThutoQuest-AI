"""
API Layer: FastAPI Routes and Pydantic Schemas
HTTP interfaces for career prediction and quest generation
"""

from fastapi import APIRouter, HTTPException, Query, Depends, status
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
from datetime import datetime
import logging

router = APIRouter(prefix="/api/v1", tags=["AI Services"])
logger = logging.getLogger(__name__)


# ============================================================================
# PYDANTIC SCHEMAS - REQUEST MODELS
# ============================================================================

class StudentProfileSchema(BaseModel):
    """Student profile request schema"""
    student_id: str = Field(..., min_length=1, max_length=50, description="Unique student identifier")
    national_id: str = Field(..., min_length=10, max_length=20, description="South African national ID")
    age: int = Field(..., ge=5, le=30, description="Student age")
    grade: int = Field(..., ge=0, le=12, description="Grade level (0=R, 12=Grade 12)")
    school: str = Field(..., min_length=1, max_length=100, description="School name")
    district: str = Field(..., min_length=1, max_length=100, description="Education district")
    
    @validator("national_id")
    def validate_national_id(cls, v):
        """Validate South African national ID format"""
        # YYMMDDSSSS... format check
        if not v.replace("-", "").isdigit():
            raise ValueError("National ID must contain only digits and hyphens")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "student_id": "STU001",
                "national_id": "050125TXXXX01",
                "age": 15,
                "grade": 10,
                "school": "Example High School",
                "district": "Gauteng"
            }
        }


class PredictCareerRequestSchema(StudentProfileSchema):
    """Career prediction request schema (extends student profile)"""
    pass


class AlternativeCareerSchema(BaseModel):
    """Alternative career option"""
    path: str = Field(..., description="Career path name")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")
    
    class Config:
        schema_extra = {
            "example": {
                "path": "data_scientist",
                "confidence": 0.75
            }
        }


class PredictCareerResponseSchema(BaseModel):
    """Career prediction response schema"""
    prediction_id: str = Field(..., description="Unique prediction ID")
    student_id: str = Field(..., description="Student ID")
    primary_career: str = Field(..., description="Primary predicted career path")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in prediction (0-1)")
    alternative_careers: List[AlternativeCareerSchema] = Field(
        ..., 
        description="Alternative career suggestions"
    )
    reasoning: Dict[str, str] = Field(
        ..., 
        description="Human-readable reasoning for prediction"
    )
    predicted_at: datetime = Field(..., description="Timestamp of prediction")
    
    class Config:
        schema_extra = {
            "example": {
                "prediction_id": "pred_abc123",
                "student_id": "STU001",
                "primary_career": "software_engineer",
                "confidence": 0.87,
                "alternative_careers": [
                    {"path": "data_scientist", "confidence": 0.75},
                    {"path": "mathematician", "confidence": 0.68}
                ],
                "reasoning": {
                    "math": "Exceptional mathematics performance",
                    "science": "Good science understanding",
                    "consistency": "Demonstrates consistent high performance",
                    "trajectory": "Positive trajectory - skills improving over time"
                },
                "predicted_at": "2026-03-20T14:30:00Z"
            }
        }


class GenerateQuestRequestSchema(StudentProfileSchema):
    """Quest generation request schema (extends student profile)"""
    pass


class GenerateQuestResponseSchema(BaseModel):
    """Quest generation response schema"""
    quest_id: str = Field(..., description="Unique quest ID")
    title: str = Field(..., max_length=200, description="Quest title")
    description: str = Field(..., max_length=500, description="Quest description")
    content: str = Field(..., description="Quest problem/challenge content")
    difficulty: str = Field(..., description="Difficulty level (beginner/intermediate/advanced/expert)")
    quest_type: str = Field(..., description="Quest type (math_problem/coding_challenge/multi_step/project_based)")
    subject: str = Field(..., description="Subject area (mathematics/coding/science)")
    topics: List[str] = Field(..., description="Topics covered in quest")
    estimated_time_minutes: int = Field(..., ge=5, le=240, description="Estimated completion time")
    points_reward: int = Field(..., ge=0, description="Points awarded on completion")
    hint: Optional[str] = Field(None, description="Optional hint for solving")
    generated_at: datetime = Field(..., description="Timestamp of generation")
    
    class Config:
        schema_extra = {
            "example": {
                "quest_id": "quest_xyz789",
                "title": "Quadratic Equations",
                "description": "Solve this intermediate mathematics problem",
                "content": "Solve x^2 - 5x + 6 = 0 using factorization",
                "difficulty": "intermediate",
                "quest_type": "math_problem",
                "subject": "mathematics",
                "topics": ["quadratic", "factorization", "roots"],
                "estimated_time_minutes": 30,
                "points_reward": 250,
                "hint": "Hint: Focus on factorization and roots concepts",
                "generated_at": "2026-03-20T14:30:00Z"
            }
        }


# ============================================================================
# PYDANTIC SCHEMAS - ERROR RESPONSES
# ============================================================================

class ErrorResponseSchema(BaseModel):
    """Standard error response"""
    error_code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "error_code": "STUDENT_NOT_FOUND",
                "message": "Student profile not found in system",
                "details": {"student_id": "STU001"},
                "timestamp": "2026-03-20T14:30:00Z"
            }
        }


class ValidationErrorSchema(BaseModel):
    """Validation error response"""
    error_code: str = "VALIDATION_ERROR"
    message: str = Field(..., description="Validation error message")
    fields: Dict[str, List[str]] = Field(..., description="Field-specific errors")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

async def get_predict_career_use_case():
    """Dependency: Career prediction use case"""
    from src.application.use_cases import PredictCareerUseCase
    from src.infrastructure.ml_models import RandomForestCareerPredictor
    from src.infrastructure.repositories import InMemoryMasteryRepository
    
    repository = InMemoryMasteryRepository()
    predictor = RandomForestCareerPredictor()
    
    return PredictCareerUseCase(
        mastery_repository=repository,
        prediction_service=predictor
    )


async def get_generate_quest_use_case():
    """Dependency: Quest generation use case"""
    from src.application.use_cases import GenerateQuestUseCase
    from src.infrastructure.ml_models import RandomForestCareerPredictor
    from src.infrastructure.rag_quest_generator import LangChainRAGQuestGenerator, DBETextbookVectorDB
    from src.infrastructure.repositories import InMemoryMasteryRepository
    
    repository = InMemoryMasteryRepository()
    predictor = RandomForestCareerPredictor()
    vector_db = DBETextbookVectorDB()
    quest_generator = LangChainRAGQuestGenerator(vector_db)
    
    return GenerateQuestUseCase(
        mastery_repository=repository,
        prediction_service=predictor,
        quest_service=quest_generator
    )


# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.get("/health", tags=["Health"])
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Returns:
        Service health status
    """
    return {
        "status": "healthy",
        "service": "ThutoQuest AI Backend",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post(
    "/predict-career",
    response_model=PredictCareerResponseSchema,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ValidationErrorSchema, "description": "Validation error"},
        404: {"model": ErrorResponseSchema, "description": "Student not found"},
        500: {"model": ErrorResponseSchema, "description": "Prediction service error"}
    }
)
async def predict_career(
    request: PredictCareerRequestSchema,
    use_case = Depends(get_predict_career_use_case)
) -> PredictCareerResponseSchema:
    """
    Predict career path for a student based on 13 years of mastery data.
    
    This endpoint uses a Random Forest classifier to analyze student performance
    across multiple subjects and predict the most suitable career path.
    
    Args:
        request: Student profile and prediction parameters
        
    Returns:
        Career prediction with confidence score and reasoning
        
    Raises:
        HTTPException: If student not found or prediction fails
        
    Example:
        ```json
        {
            "student_id": "STU001",
            "national_id": "050125TXXXX01",
            "age": 15,
            "grade": 10,
            "school": "Example High School",
            "district": "Gauteng"
        }
        ```
    """
    try:
        from src.application.use_cases import PredictCareerRequest
        
        # Convert schema to use case request
        use_case_request = PredictCareerRequest(
            student_id=request.student_id,
            national_id=request.national_id,
            age=request.age,
            grade=request.grade,
            school=request.school,
            district=request.district
        )
        
        # Execute use case
        response = await use_case.execute(use_case_request)
        
        # Convert use case response to schema
        return PredictCareerResponseSchema(
            prediction_id=response.prediction_id,
            student_id=response.student_id,
            primary_career=response.primary_career,
            confidence=response.confidence,
            alternative_careers=[
                AlternativeCareerSchema(path=c["path"], confidence=c["confidence"])
                for c in response.alternative_careers
            ],
            reasoning=response.reasoning,
            predicted_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Career prediction error: {str(e)}")
        
        # Handle specific exceptions
        from src.domain.models import StudentNotFoundError, InvalidMasteryDataError, PredictionFailedError
        
        if isinstance(e, StudentNotFoundError):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error_code": "STUDENT_NOT_FOUND",
                    "message": str(e),
                    "student_id": request.student_id
                }
            )
        elif isinstance(e, InvalidMasteryDataError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error_code": "INVALID_DATA",
                    "message": str(e)
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error_code": "PREDICTION_ERROR",
                    "message": "Career prediction failed - please try again"
                }
            )


@router.post(
    "/generate-quest",
    response_model=GenerateQuestResponseSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ValidationErrorSchema, "description": "Validation error"},
        404: {"model": ErrorResponseSchema, "description": "Student not found"},
        500: {"model": ErrorResponseSchema, "description": "Generation service error"}
    }
)
async def generate_quest(
    request: GenerateQuestRequestSchema,
    use_case = Depends(get_generate_quest_use_case)
) -> GenerateQuestResponseSchema:
    """
    Generate a personalized quest for a student using RAG.
    
    This endpoint uses LangChain and RAG (Retrieval-Augmented Generation) to 
    fetch relevant math/coding challenges from a vector database of DBE textbooks
    and generate personalized quests aligned with the student's mastery profile.
    
    Args:
        request: Student profile for quest generation
        
    Returns:
        Generated quest with difficulty, content, and metadata
        
    Raises:
        HTTPException: If student not found or quest generation fails
        
    Example:
        ```json
        {
            "student_id": "STU001",
            "national_id": "050125TXXXX01",
            "age": 15,
            "grade": 10,
            "school": "Example High School",
            "district": "Gauteng"
        }
        ```
    """
    try:
        from src.application.use_cases import GenerateQuestRequest
        
        # Convert schema to use case request
        use_case_request = GenerateQuestRequest(
            student_id=request.student_id,
            national_id=request.national_id,
            age=request.age,
            grade=request.grade,
            school=request.school,
            district=request.district
        )
        
        # Execute use case
        response = await use_case.execute(use_case_request)
        
        # Convert use case response to schema
        return GenerateQuestResponseSchema(
            quest_id=response.quest_id,
            title=response.title,
            description=response.description,
            content=response.content,
            difficulty=response.difficulty,
            quest_type=response.quest_type,
            subject=response.subject,
            topics=response.topics,
            estimated_time_minutes=response.estimated_time_minutes,
            points_reward=response.points_reward,
            hint=response.hint,
            generated_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Quest generation error: {str(e)}")
        
        # Handle specific exceptions
        from src.domain.models import StudentNotFoundError, InvalidMasteryDataError, QuestGenerationError
        
        if isinstance(e, StudentNotFoundError):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error_code": "STUDENT_NOT_FOUND",
                    "message": str(e),
                    "student_id": request.student_id
                }
            )
        elif isinstance(e, InvalidMasteryDataError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error_code": "INVALID_DATA",
                    "message": str(e)
                }
            )
        elif isinstance(e, QuestGenerationError):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error_code": "GENERATION_ERROR",
                    "message": str(e)
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "error_code": "QUEST_ERROR",
                    "message": "Quest generation failed - please try again"
                }
            )


@router.get(
    "/predict-career/{student_id}",
    response_model=PredictCareerResponseSchema,
    status_code=status.HTTP_200_OK
)
async def get_prediction(student_id: str) -> PredictCareerResponseSchema:
    """
    Retrieve a previously generated career prediction.
    
    Args:
        student_id: Unique student identifier
        
    Returns:
        Previously generated career prediction
    """
    # TODO: Implement retrieval from persistence layer
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Prediction retrieval endpoint coming soon"
    )


@router.get(
    "/quests/{student_id}",
    response_model=List[GenerateQuestResponseSchema],
    status_code=status.HTTP_200_OK
)
async def get_student_quests(
    student_id: str,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
) -> List[GenerateQuestResponseSchema]:
    """
    Retrieve all quests generated for a student.
    
    Args:
        student_id: Unique student identifier
        limit: Maximum number of quests to return
        offset: Number of quests to skip (for pagination)
        
    Returns:
        List of quests for the student
    """
    # TODO: Implement quest retrieval from persistence layer
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Quest retrieval endpoint coming soon"
    )
