"""
Unit Tests for Phase 2: Gamification System
Comprehensive tests for achievements, leaderboards, and gamification features
"""

import pytest
from uuid import UUID
from datetime import datetime, timedelta

from src.domain.gamification import (
    LeaderboardCalculator,
    AchievementUnlocker,
    ACHIEVEMENT_DEFINITIONS,
    AchievementUnlockCondition,
    StudentGamificationProfile
)


# ============================================================================
# ACHIEVEMENT UNLOCK TESTS
# ============================================================================

class TestAchievementUnlock:
    """Tests for achievement unlock conditions"""
    
    def test_mastery_threshold_wizard(self):
        """Test Math Wizard achievement unlock at 0.9 mastery"""
        result = AchievementUnlocker.check_mastery_threshold(
            student_id="student1",
            concept="Mathematics",
            current_mastery=0.95,
            achievement_key="math_wizard"
        )
        assert result is True, "Math Wizard should unlock at 0.95 mastery"
    
    def test_mastery_threshold_not_unlocked(self):
        """Test achievement doesn't unlock below threshold"""
        result = AchievementUnlocker.check_mastery_threshold(
            student_id="student1",
            concept="Mathematics",
            current_mastery=0.85,
            achievement_key="math_wizard"
        )
        assert result is False, "Math Wizard should NOT unlock at 0.85 mastery"
    
    def test_consecutive_success_ace(self):
        """Test Accuracy Ace achievement unlock"""
        result = AchievementUnlocker.check_consecutive_success(
            correct_count=12,
            achievement_key="accuracy_ace"
        )
        assert result is True, "Accuracy Ace should unlock at 12 consecutive"
    
    def test_consecutive_success_below_threshold(self):
        """Test consecutive success doesn't unlock below threshold"""
        result = AchievementUnlocker.check_consecutive_success(
            correct_count=5,
            achievement_key="accuracy_ace"
        )
        assert result is False, "Accuracy Ace should NOT unlock at 5 consecutive"
    
    def test_perseverance_champion(self):
        """Test Persistence Champion achievement unlock"""
        result = AchievementUnlocker.check_perseverance(
            attempts=65,
            achievement_key="persistence_champion"
        )
        assert result is True, "Persistence Champion should unlock at 65 attempts"
    
    def test_perseverance_below_threshold(self):
        """Test perseverance doesn't unlock below threshold"""
        result = AchievementUnlocker.check_perseverance(
            attempts=30,
            achievement_key="persistence_champion"
        )
        assert result is False, "Persistence Champion should NOT unlock at 30 attempts"
    
    def test_get_unlockable_achievements(self):
        """Test getting list of potentially unlockable achievements"""
        unlockable = AchievementUnlocker.get_unlockable_achievements(
            mastery_score=0.92,
            attempt_count=56,
            achievement_count=0,
            hours_spent=60.0
        )
        
        # Should unlock achievements matching criteria
        assert "accuracy_ace" in unlockable or len(unlockable) >= 1
        assert isinstance(unlockable, list)
        assert len(unlockable) > 0, "Should have unlockable achievements"


# ============================================================================
# LEADERBOARD CALCULATION TESTS
# ============================================================================

class TestLeaderboardCalculator:
    """Tests for leaderboard score calculations and rankings"""
    
    def test_calculate_leaderboard_score_high_performer(self):
        """Test score calculation for high achiever"""
        score = LeaderboardCalculator.calculate_leaderboard_score(
            mastery_score=0.95,
            achievement_count=10,
            time_on_task_hours=50,
            improvement_rate=0.8,
            max_achievements=50
        )
        
        assert score > 7000, f"High performer should score > 7000, got {score}"
        assert score <= 10000, "Score should not exceed 10000"
    
    def test_calculate_leaderboard_score_low_performer(self):
        """Test score calculation for struggling student"""
        score = LeaderboardCalculator.calculate_leaderboard_score(
            mastery_score=0.40,
            achievement_count=1,
            time_on_task_hours=5,
            improvement_rate=0.1,
            max_achievements=50
        )
        
        assert score < 3000, f"Low performer should score < 3000, got {score}"
        assert score >= 0, "Score should not be negative"
    
    def test_score_weight_distribution(self):
        """Test that score weights are applied correctly"""
        # Same mastery, different achievements should show difference
        score1 = LeaderboardCalculator.calculate_leaderboard_score(
            mastery_score=0.80,
            achievement_count=5,
            time_on_task_hours=20,
            improvement_rate=0.5
        )
        
        score2 = LeaderboardCalculator.calculate_leaderboard_score(
            mastery_score=0.80,
            achievement_count=15,  # Higher achievements
            time_on_task_hours=20,
            improvement_rate=0.5
        )
        
        assert score2 > score1, "More achievements should yield higher score"
    
    def test_rank_students_correct_order(self):
        """Test that students are ranked correctly"""
        scores = [
            (UUID("00000000-0000-0000-0000-000000000001"), "Alice", "School A", 5000, 0.85, 5),
            (UUID("00000000-0000-0000-0000-000000000002"), "Bob", "School B", 8000, 0.95, 8),
            (UUID("00000000-0000-0000-0000-000000000003"), "Charlie", "School A", 3000, 0.70, 2),
        ]
        
        ranked = LeaderboardCalculator.rank_students(scores)
        
        assert len(ranked) == 3, "Should have 3 ranked entries"
        assert ranked[0].student_name == "Bob", "Bob should be rank 1"
        assert ranked[0].rank == 1, "First entry should have rank 1"
        assert ranked[1].student_name == "Alice", "Alice should be rank 2"
        assert ranked[2].student_name == "Charlie", "Charlie should be rank 3"
    
    def test_rank_preserves_metadata(self):
        """Test that ranking preserves all student metadata"""
        scores = [
            (UUID("00000000-0000-0000-0000-000000000001"), "Test Student", "Test School", 5000, 0.85, 5),
        ]
        
        ranked = LeaderboardCalculator.rank_students(scores)
        entry = ranked[0]
        
        assert entry.student_name == "Test Student"
        assert entry.school == "Test School"
        assert entry.points == 5000
        assert entry.mastery_score == 0.85
        assert entry.achievements_earned == 5
    
    def test_score_normalization(self):
        """Test that very high values are normalized"""
        # Test with very high stats
        score = LeaderboardCalculator.calculate_leaderboard_score(
            mastery_score=1.0,
            achievement_count=1000,  # Extremely high
            time_on_task_hours=10000,  # Extremely high
            improvement_rate=2.0  # Above max
        )
        
        assert score <= 10000, "Score should be capped at 10000"


# ============================================================================
# ACHIEVEMENT DEFINITIONS TESTS
# ============================================================================

class TestAchievementDefinitions:
    """Tests for achievement definitions and configuration"""
    
    def test_all_achievements_have_required_fields(self):
        """Test that all achievements have required metadata"""
        required_fields = {"name", "description", "icon", "rarity", "points", "unlock"}
        
        for key, achievement in ACHIEVEMENT_DEFINITIONS.items():
            missing = required_fields - set(achievement.keys())
            assert not missing, f"Achievement '{key}' missing fields: {missing}"
    
    def test_achievement_points_are_positive(self):
        """Test that all achievements award positive points"""
        for key, achievement in ACHIEVEMENT_DEFINITIONS.items():
            assert achievement["points"] > 0, f"Achievement '{key}' has non-positive points"
            assert achievement["points"] <= 10000, f"Achievement '{key}' has unreasonable points"
    
    def test_unlock_conditions_are_valid(self):
        """Test that unlock conditions have proper structure"""
        for key, achievement in ACHIEVEMENT_DEFINITIONS.items():
            unlock = achievement["unlock"]
            assert isinstance(unlock, dict), f"Unlock for '{key}' should be dict"
            assert "type" in unlock, f"Unlock for '{key}' missing 'type' field"
    
    def test_achievement_definitions_not_empty(self):
        """Test that achievements are defined"""
        assert len(ACHIEVEMENT_DEFINITIONS) > 0, "No achievements defined"
        assert len(ACHIEVEMENT_DEFINITIONS) >= 8, "Should have at least 8 achievements"


# ============================================================================
# UNLOCK CONDITION TESTS
# ============================================================================

class TestAchievementUnlockCondition:
    """Tests for unlock condition builders"""
    
    def test_mastery_threshold_condition(self):
        """Test building mastery threshold condition"""
        condition = AchievementUnlockCondition.mastery_threshold("Math", 0.85)
        
        assert condition["type"] == "mastery_threshold"
        assert condition["concept"] == "Math"
        assert condition["threshold"] == 0.85
    
    def test_consecutive_success_condition(self):
        """Test building consecutive success condition"""
        condition = AchievementUnlockCondition.consecutive_success(15)
        
        assert condition["type"] == "consecutive_success"
        assert condition["consecutive_correct"] == 15
    
    def test_time_investment_condition(self):
        """Test building time investment condition"""
        condition = AchievementUnlockCondition.time_investment(100)
        
        assert condition["type"] == "time_investment"
        assert condition["hours"] == 100


# ============================================================================
# GAMIFICATION PROFILE TESTS
# ============================================================================

class TestStudentGamificationProfile:
    """Tests for student gamification profile calculations"""
    
    @pytest.fixture
    def sample_profile(self):
        """Create a sample profile for testing"""
        from uuid import uuid4
        return StudentGamificationProfile(
            student_id=uuid4(),
            total_points=5000,
            achievement_count=5,
            leaderboard_ranks={"national": 42, "school": 8, "subject_math": 15},
            current_streak=7,
            total_hours_spent=25.5,
            total_attempts=235,
            achievements=[],
            recent_achievements=[]
        )
    
    def test_get_engagement_level_dedicated(self):
        """Test engagement level for 50+ hours"""
        profile = StudentGamificationProfile(
            student_id=UUID("00000000-0000-0000-0000-000000000001"),
            total_points=0, achievement_count=0, leaderboard_ranks={},
            current_streak=0, total_hours_spent=75.0, total_attempts=0,
            achievements=[], recent_achievements=[]
        )
        
        assert profile.get_engagement_level() == "Dedicated"
    
    def test_get_engagement_level_regular(self):
        """Test engagement level for 25-50 hours"""
        profile = StudentGamificationProfile(
            student_id=UUID("00000000-0000-0000-0000-000000000001"),
            total_points=0, achievement_count=0, leaderboard_ranks={},
            current_streak=0, total_hours_spent=30.0, total_attempts=0,
            achievements=[], recent_achievements=[]
        )
        
        assert profile.get_engagement_level() == "Regular"
    
    def test_get_engagement_level_casual(self):
        """Test engagement level for 5-25 hours"""
        profile = StudentGamificationProfile(
            student_id=UUID("00000000-0000-0000-0000-000000000001"),
            total_points=0, achievement_count=0, leaderboard_ranks={},
            current_streak=0, total_hours_spent=10.0, total_attempts=0,
            achievements=[], recent_achievements=[]
        )
        
        assert profile.get_engagement_level() == "Casual"
    
    def test_get_level_calculation(self):
        """Test player level calculation (1000 points per level)"""
        profile = StudentGamificationProfile(
            student_id=UUID("00000000-0000-0000-0000-000000000001"),
            total_points=7500, achievement_count=0, leaderboard_ranks={},
            current_streak=0, total_hours_spent=0, total_attempts=0,
            achievements=[], recent_achievements=[]
        )
        
        assert profile.get_level() == 7, "7500 points should equal level 7"
    
    def test_get_next_level_progress(self):
        """Test progress to next level"""
        profile = StudentGamificationProfile(
            student_id=UUID("00000000-0000-0000-0000-000000000001"),
            total_points=7500, achievement_count=0, leaderboard_ranks={},
            current_streak=0, total_hours_spent=0, total_attempts=0,
            achievements=[], recent_achievements=[]
        )
        
        progress = profile.get_next_level_progress()
        
        # 7500 points = 7 levels, within level 7
        # Current level = 7, next = 8
        # Points for level 7: 7000, for level 8: 8000
        # Progress: (7500 - 7000) / (8000 - 7000) = 500/1000 = 0.5
        assert 0.49 <= progress <= 0.51, f"Progress should be ~0.5, got {progress}"
    
    def test_get_next_level_progress_clamping(self):
        """Test that progress is clamped between 0.0 and 1.0"""
        # Very low points
        profile_low = StudentGamificationProfile(
            student_id=UUID("00000000-0000-0000-0000-000000000001"),
            total_points=100, achievement_count=0, leaderboard_ranks={},
            current_streak=0, total_hours_spent=0, total_attempts=0,
            achievements=[], recent_achievements=[]
        )
        
        assert 0.0 <= profile_low.get_next_level_progress() <= 1.0
        
        # Very high points
        profile_high = StudentGamificationProfile(
            student_id=UUID("00000000-0000-0000-0000-000000000001"),
            total_points=100000, achievement_count=0, leaderboard_ranks={},
            current_streak=0, total_hours_spent=0, total_attempts=0,
            achievements=[], recent_achievements=[]
        )
        
        assert 0.0 <= profile_high.get_next_level_progress() <= 1.0


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestGamificationIntegration:
    """Integration tests combining multiple gamification components"""
    
    def test_achievement_and_score_interaction(self):
        """Test that achievements affect leaderboard scoring"""
        base_score = LeaderboardCalculator.calculate_leaderboard_score(
            mastery_score=0.80,
            achievement_count=2,
            time_on_task_hours=20,
            improvement_rate=0.5
        )
        
        higher_achievement_score = LeaderboardCalculator.calculate_leaderboard_score(
            mastery_score=0.80,
            achievement_count=8,
            time_on_task_hours=20,
            improvement_rate=0.5
        )
        
        assert higher_achievement_score > base_score, \
            "More achievements should increase leaderboard score"
    
    def test_profile_metrics_consistency(self):
        """Test that profile metrics are internally consistent"""
        profile = StudentGamificationProfile(
            student_id=UUID("00000000-0000-0000-0000-000000000001"),
            total_points=8500,
            achievement_count=8,
            leaderboard_ranks={"national": 1},
            current_streak=14,
            total_hours_spent=45.0,
            total_attempts=456,
            achievements=[],
            recent_achievements=[]
        )
        
        # High engagement metrics should correspond
        assert profile.get_engagement_level() == "Regular"
        assert profile.get_level() >= 8
        assert profile.current_streak > 0
