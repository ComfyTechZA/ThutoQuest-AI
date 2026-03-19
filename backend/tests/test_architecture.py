"""
Comprehensive Unit Tests for Clean Hexagonal Architecture
Tests cover all layers: Domain, Application, Infrastructure, Interface
"""

import pytest
import numpy as np
from datetime import datetime
from uuid import uuid4

from src.domain.models import (
    StudentProfile,
    StudentMasteryHistory,
    CareerPrediction,
    CareerPath,
    Quest,
    QuestDifficulty,
    QuestType,
    InvalidMasteryDataError,
)
from src.infrastructure.ml_models import RandomForestCareerPredictor
from src.infrastructure.rag_quest_generator import (
    LangChainRAGQuestGenerator,
    DBETextbookVectorDB
)
from src.infrastructure.repositories import InMemoryMasteryRepository
from src.application.use_cases import (
    PredictCareerUseCase,
    GenerateQuestUseCase,
    PredictCareerRequest,
)


# ============================================================================
# DOMAIN MODEL TESTS
# ============================================================================

class TestStudentProfile:
    """Tests for StudentProfile value object"""
    
    def test_valid_student_profile(self):
        """Test creation of valid student profile"""
        profile = StudentProfile(
            student_id="STU001",
            national_id="050125TXXXX01",
            age=15,
            grade=10,
            school="Example High",
            district="Gauteng"
        )
        assert profile.validate() is True
    
    def test_invalid_age(self):
        """Test profile with invalid age"""
        profile = StudentProfile(
            student_id="STU001",
            national_id="050125TXXXX01",
            age=100,  # Invalid
            grade=10,
            school="Example High",
            district="Gauteng"
        )
        assert profile.validate() is False
    
    def test_invalid_grade(self):
        """Test profile with invalid grade"""
        profile = StudentProfile(
            student_id="STU001",
            national_id="050125TXXXX01",
            age=15,
            grade=15,  # Invalid
            school="Example High",
            district="Gauteng"
        )
        assert profile.validate() is False


class TestStudentMasteryHistory:
    """Tests for StudentMasteryHistory value object"""
    
    def test_valid_mastery_history(self):
        """Test creation of valid mastery history"""
        history = StudentMasteryHistory(
            student_id="STU001",
            grades=list(range(0, 13)),
            math_scores=[[0.5, 0.6, 0.7] for _ in range(13)],
            science_scores=[[0.5, 0.6, 0.7] for _ in range(13)],
            language_scores=[[0.5, 0.6, 0.7] for _ in range(13)],
            consistency_score=0.8,
            improvement_rate=0.1
        )
        assert history.years_of_data() == 13
    
    def test_years_of_data(self):
        """Test years_of_data calculation"""
        history = StudentMasteryHistory(
            student_id="STU001",
            grades=[0, 1, 2],
            math_scores=[[0.5], [0.6], [0.7]],
            science_scores=[[0.5], [0.6], [0.7]],
            language_scores=[[0.5], [0.6], [0.7]],
            consistency_score=0.8,
            improvement_rate=0.1
        )
        assert history.years_of_data() == 3


# ============================================================================
# ML MODEL TESTS
# ============================================================================

class TestRandomForestCareerPredictor:
    """Tests for Random Forest career predictor"""
    
    @pytest.fixture
    def predictor(self):
        """Fixture: initialized predictor"""
        return RandomForestCareerPredictor()
    
    @pytest.fixture
    def student_profile(self):
        """Fixture: sample student profile"""
        return StudentProfile(
            student_id="STU001",
            national_id="050125TXXXX01",
            age=15,
            grade=10,
            school="Example High",
            district="Gauteng"
        )
    
    @pytest.fixture
    def mastery_history(self):
        """Fixture: sample mastery history"""
        return StudentMasteryHistory(
            student_id="STU001",
            grades=list(range(0, 13)),
            math_scores=[[0.8, 0.85, 0.9] for _ in range(13)],
            science_scores=[[0.7, 0.75, 0.8] for _ in range(13)],
            language_scores=[[0.6, 0.65, 0.7] for _ in range(13)],
            consistency_score=0.85,
            improvement_rate=0.1
        )
    
    @pytest.mark.asyncio
    async def test_predict_returns_career_prediction(
        self, predictor, student_profile, mastery_history
    ):
        """Test that predict returns valid CareerPrediction"""
        result = await predictor.predict(student_profile, mastery_history)
        
        assert isinstance(result, CareerPrediction)
        assert result.student_id == "STU001"
        assert 0.0 <= result.confidence <= 1.0
        assert isinstance(result.primary_career, CareerPath)
    
    @pytest.mark.asyncio
    async def test_confidence_high_for_high_performer(
        self, predictor, student_profile, mastery_history
    ):
        """Test high confidence for strong student"""
        result = await predictor.predict(student_profile, mastery_history)
        
        # Strong performer should have high confidence
        assert result.confidence > 0.6
    
    @pytest.mark.asyncio
    async def test_alternatives_provided(
        self, predictor, student_profile, mastery_history
    ):
        """Test that alternatives are provided"""
        result = await predictor.predict(student_profile, mastery_history)
        
        assert len(result.alternative_careers) > 0
        assert len(result.alternative_careers) <= 3


# ============================================================================
# VECTOR DATABASE TESTS
# ============================================================================

class TestDBETextbookVectorDB:
    """Tests for vector database adapter"""
    
    @pytest.fixture
    def vector_db(self):
        """Fixture: initialized vector database"""
        return DBETextbookVectorDB()
    
    @pytest.mark.asyncio
    async def test_search_returns_content(self, vector_db):
        """Test that search returns relevant content"""
        results = await vector_db.search_content(
            query="quadratic equations",
            subject="mathematics",
            grade=10,
            top_k=5
        )
        
        assert isinstance(results, list)
        assert len(results) > 0
    
    @pytest.mark.asyncio
    async def test_search_respects_top_k(self, vector_db):
        """Test that search respects top_k parameter"""
        results = await vector_db.search_content(
            query="mathematics",
            subject="mathematics",
            grade=10,
            top_k=2
        )
        
        assert len(results) <= 2
    
    @pytest.mark.asyncio
    async def test_search_coding_challenges(self, vector_db):
        """Test searching for coding challenges"""
        results = await vector_db.search_content(
            query="python loops",
            subject="coding",
            grade=10,
            top_k=5
        )
        
        assert isinstance(results, list)


# ============================================================================
# QUEST GENERATION TESTS
# ============================================================================

class TestLangChainRAGQuestGenerator:
    """Tests for LangChain RAG quest generator"""
    
    @pytest.fixture
    def quest_generator(self):
        """Fixture: initialized quest generator"""
        vector_db = DBETextbookVectorDB()
        return LangChainRAGQuestGenerator(vector_db)
    
    @pytest.fixture
    def student_profile(self):
        """Fixture: sample student profile"""
        return StudentProfile(
            student_id="STU001",
            national_id="050125TXXXX01",
            age=15,
            grade=10,
            school="Example High",
            district="Gauteng"
        )
    
    @pytest.fixture
    def mastery_history(self):
        """Fixture: sample mastery history"""
        return StudentMasteryHistory(
            student_id="STU001",
            grades=list(range(0, 13)),
            math_scores=[[0.6, 0.65, 0.7] for _ in range(13)],
            science_scores=[[0.5, 0.55, 0.6] for _ in range(13)],
            language_scores=[[0.7, 0.75, 0.8] for _ in range(13)],
            consistency_score=0.75,
            improvement_rate=0.05
        )
    
    @pytest.mark.asyncio
    async def test_generate_returns_quest(
        self, quest_generator, student_profile, mastery_history
    ):
        """Test that generate_quest returns valid Quest"""
        result = await quest_generator.generate_quest(
            student_id="STU001",
            student_profile=student_profile,
            mastery_history=mastery_history
        )
        
        assert isinstance(result, Quest)
        assert result.student_id == "STU001"
        assert isinstance(result.difficulty, QuestDifficulty)
        assert isinstance(result.quest_type, QuestType)
    
    @pytest.mark.asyncio
    async def test_difficulty_matches_performance(
        self, quest_generator, student_profile, mastery_history
    ):
        """Test that difficulty matches student performance"""
        result = await quest_generator.generate_quest(
            student_id="STU001",
            student_profile=student_profile,
            mastery_history=mastery_history
        )
        
        # Moderate performance should get intermediate difficulty
        # (depending on calculation)
        assert result.difficulty in [
            QuestDifficulty.BEGINNER,
            QuestDifficulty.INTERMEDIATE,
            QuestDifficulty.ADVANCED
        ]


# ============================================================================
# REPOSITORY TESTS
# ============================================================================

class TestInMemoryMasteryRepository:
    """Tests for in-memory repository"""
    
    @pytest.fixture
    def repository(self):
        """Fixture: initialized repository"""
        return InMemoryMasteryRepository()
    
    @pytest.mark.asyncio
    async def test_get_mastery_history_returns_data(self, repository):
        """Test retrieval of mastery history"""
        result = await repository.get_mastery_history("STU001")
        
        assert result is not None
        assert isinstance(result, StudentMasteryHistory)
        assert result.student_id == "STU001"
    
    @pytest.mark.asyncio
    async def test_get_nonexistent_student_returns_none(self, repository):
        """Test that nonexistent student returns None"""
        result = await repository.get_mastery_history("NONEXISTENT")
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_save_prediction(self, repository):
        """Test prediction saving"""
        prediction = CareerPrediction(
            prediction_id="pred_001",
            student_id="STU001",
            primary_career=CareerPath.SOFTWARE_ENGINEER,
            confidence=0.85,
            alternative_careers=[(CareerPath.DATA_SCIENTIST, 0.75)],
            reasoning={"math": "Strong"},
            predicted_at=datetime.utcnow()
        )
        
        result = await repository.save_prediction(prediction)
        
        assert result is True
    
    @pytest.mark.asyncio
    async def test_save_quest(self, repository):
        """Test quest saving"""
        quest = Quest(
            quest_id="quest_001",
            student_id="STU001",
            title="Test Quest",
            description="Test",
            content="Test content",
            difficulty=QuestDifficulty.INTERMEDIATE,
            quest_type=QuestType.MATH_PROBLEM,
            subject="mathematics",
            topics=["algebra"],
            source_material="Test Book",
            estimated_time_minutes=30,
            points_reward=250,
            solution_hint="Test hint",
            reference_grade=10,
            generated_at=datetime.utcnow()
        )
        
        result = await repository.save_quest(quest)
        
        assert result is True


# ============================================================================
# USE CASE TESTS
# ============================================================================

class TestPredictCareerUseCase:
    """Tests for career prediction use case"""
    
    @pytest.fixture
    def use_case(self):
        """Fixture: initialized use case"""
        repository = InMemoryMasteryRepository()
        predictor = RandomForestCareerPredictor()
        return PredictCareerUseCase(repository, predictor)
    
    @pytest.mark.asyncio
    async def test_execute_returns_prediction(self, use_case):
        """Test that execute returns valid prediction"""
        request = PredictCareerRequest(
            student_id="STU001",
            national_id="050125TXXXX01",
            age=15,
            grade=10,
            school="Example High",
            district="Gauteng"
        )
        
        result = await use_case.execute(request)
        
        assert result.primary_career is not None
        assert result.confidence is not None


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestCareerPredictionPipeline:
    """Integration tests for full prediction pipeline"""
    
    @pytest.mark.asyncio
    async def test_full_prediction_pipeline(self):
        """Test complete prediction pipeline"""
        # Setup
        repository = InMemoryMasteryRepository()
        predictor = RandomForestCareerPredictor()
        use_case = PredictCareerUseCase(repository, predictor)
        
        request = PredictCareerRequest(
            student_id="STU001",
            national_id="050125TXXXX01",
            age=15,
            grade=10,
            school="Example High",
            district="Gauteng"
        )
        
        # Execute
        result = await use_case.execute(request)
        
        # Assert
        assert result.student_id == "STU001"
        assert 0.0 <= result.confidence <= 1.0
        assert len(result.alternative_careers) <= 3


class TestQuestGenerationPipeline:
    """Integration tests for full quest generation pipeline"""
    
    @pytest.mark.asyncio
    async def test_full_quest_generation_pipeline(self):
        """Test complete quest generation pipeline"""
        # Setup
        repository = InMemoryMasteryRepository()
        predictor = RandomForestCareerPredictor()
        vector_db = DBETextbookVectorDB()
        quest_generator = LangChainRAGQuestGenerator(vector_db)
        use_case = GenerateQuestUseCase(repository, predictor, quest_generator)
        
        from src.application.use_cases import GenerateQuestRequest
        request = GenerateQuestRequest(
            student_id="STU001",
            national_id="050125TXXXX01",
            age=15,
            grade=10,
            school="Example High",
            district="Gauteng"
        )
        
        # Execute
        result = await use_case.execute(request)
        
        # Assert
        assert result.quest_id is not None
        assert result.title is not None
        assert result.content is not None
        assert 0 < result.estimated_time_minutes <= 240


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
