"""
Unit Tests for Grade 10 Critical Gap Detection Logic
Tests ensure the gap-detection system correctly identifies struggling students
and recommends appropriate interventions.
"""

import pytest
from src.domain.grade10_logic import (
    Grade10CriticalGapAnalyzer,
    MasteryData,
    CriticalGap,
    BossBattleQuest,
    check_algebraic_expressions_gap
)


class TestGrade10CriticalGapAnalyzer:
    """Test suite for Grade10CriticalGapAnalyzer"""
    
    @pytest.fixture
    def analyzer(self):
        """Fixture providing a fresh analyzer instance for each test"""
        return Grade10CriticalGapAnalyzer()
    
    def test_identify_algebraic_expressions_gap_below_threshold(self, analyzer):
        """
        Test that students with Algebraic Expressions mastery < 0.5 are identified as having critical gaps.
        
        This test verifies the core functionality: identifying students who need the
        'Expression Guardian' Boss Battle quest for foundational math concepts.
        
        Expected behavior:
        - A student with mastery_score = 0.35 < 0.5 threshold
        - Should be identified as having a critical gap
        - Gap type should be FOUNDATIONAL
        - Severity should be 5 (highest)
        """
        # Arrange
        student_id = "student_001"
        mastery_data = [
            MasteryData(
                student_id=student_id,
                curriculum_node="Algebraic Expressions",
                mastery_score=0.35,  # Below critical threshold of 0.5
                attempts=3
            )
        ]
        
        # Act
        gaps = analyzer.identify_critical_gaps(mastery_data)
        
        # Assert
        assert len(gaps) == 1, "Should identify exactly one critical gap"
        assert gaps[0].student_id == student_id
        assert gaps[0].node_name == "Algebraic Expressions"
        assert gaps[0].mastery_score == 0.35
        assert gaps[0].severity == 5, "Algebraic Expressions should have highest severity"
        assert "Boss Battle" in gaps[0].recommended_action
    
    def test_no_gap_for_mastery_above_threshold(self, analyzer):
        """
        Test that students with mastery >= 0.5 are NOT flagged as having critical gaps.
        
        This test ensures the gap-detection system doesn't produce false positives.
        Students performing adequately (>= 0.5) should not receive intervention quests.
        
        Expected behavior:
        - A student with mastery_score = 0.65 >= 0.5 threshold
        - Should NOT be identified as having a critical gap
        - No remedial quest should be generated
        """
        # Arrange
        student_id = "student_002"
        mastery_data = [
            MasteryData(
                student_id=student_id,
                curriculum_node="Algebraic Expressions",
                mastery_score=0.65,  # Above critical threshold of 0.5
                attempts=2
            )
        ]
        
        # Act
        gaps = analyzer.identify_critical_gaps(mastery_data)
        
        # Assert
        assert len(gaps) == 0, "Should identify no critical gaps for score above threshold"
    
    def test_boss_battle_quest_generation_for_struggling_student(self, analyzer):
        """
        Test that appropriate Boss Battle quests are generated for students with gaps.
        
        This test verifies the quest generation system creates meaningful interventions
        with correct objectives, rewards, and difficulty levels for struggling students.
        
        Expected behavior:
        - Student has critical gap in Equations and Inequalities (mastery = 0.4)
        - Boss Battle quest should be generated
        - Quest should include proper objectives and reward points (600+ for severity 5)
        - Boss name should match the concept
        """
        # Arrange
        student_id = "student_003"
        mastery_data = [
            MasteryData(
                student_id=student_id,
                curriculum_node="Equations and Inequalities",
                mastery_score=0.4,  # Below threshold, triggers Boss Battle
                attempts=1
            )
        ]
        
        # Act
        gaps = analyzer.identify_critical_gaps(mastery_data)
        boss_battles = analyzer.generate_boss_battle_quests(gaps)
        
        # Assert
        assert len(boss_battles) == 1, "Should generate one Boss Battle quest"
        
        quest = boss_battles[0]
        assert quest.student_id == student_id
        assert quest.failed_concept == "Equations and Inequalities"
        assert quest.boss_name == "The Balance Keeper"
        assert len(quest.objectives) > 0, "Quest should have learning objectives"
        assert quest.reward_points >= 600, "High-severity quest should reward 600+ points"
        assert quest.difficulty == "Hard"
        assert quest.quest_id.startswith("boss_battle_")
    
    def test_analyze_student_comprehensive_report(self, analyzer):
        """
        Test comprehensive student analysis producing complete gap and quest report.
        
        This test verifies the full student analysis workflow, checking that the system
        correctly aggregates multiple mastery records and provides actionable insights.
        
        Expected behavior:
        - Student with 2 critical gaps: Algebraic Expressions (0.3) and Functions (0.45)
        - Analysis should identify both gaps
        - Two Boss Battle quests should be generated
        - Report should include all recommendations
        """
        # Arrange
        student_id = "student_004"
        mastery_records = [
            MasteryData(
                student_id=student_id,
                curriculum_node="Algebraic Expressions",
                mastery_score=0.3,
                attempts=2
            ),
            MasteryData(
                student_id=student_id,
                curriculum_node="Functions",
                mastery_score=0.45,
                attempts=1
            ),
            MasteryData(
                student_id=student_id,
                curriculum_node="Graphs and Transformations",
                mastery_score=0.75,  # Acceptable performance
                attempts=3
            )
        ]
        
        # Act
        analysis = analyzer.analyze_student(student_id, mastery_records)
        
        # Assert
        assert analysis["student_id"] == student_id
        assert analysis["has_critical_gaps"] is True
        assert analysis["total_gaps"] == 2, "Should identify 2 critical gaps"
        assert len(analysis["critical_gaps"]) == 2
        assert len(analysis["boss_battle_quests"]) == 2
        
        # Verify gap concepts
        gap_concepts = [gap["concept"] for gap in analysis["critical_gaps"]]
        assert "Algebraic Expressions" in gap_concepts
        assert "Functions" in gap_concepts
        
        # Verify Boss Battle names
        boss_names = [quest["boss_name"] for quest in analysis["boss_battle_quests"]]
        assert "The Expression Guardian" in boss_names
        assert "The Function Master" in boss_names
    
    def test_multiple_students_with_varying_profiles(self, analyzer):
        """
        Test gap detection across multiple students with different performance profiles.
        
        This test ensures the system correctly processes diverse student backgrounds
        and identifies gaps appropriately for each individual.
        
        Expected behavior:
        - Student A: High achiever (>= 0.8) - no gaps
        - Student B: Struggling (< 0.5) - identified with gaps
        - Student C: Average (0.5-0.7) - no gaps
        - System should return correct counts for each
        """
        # Arrange
        mastery_data = [
            # Student A: High achiever
            MasteryData("student_A", "Algebraic Expressions", 0.85, 4),
            MasteryData("student_A", "Functions", 0.9, 3),
            
            # Student B: Struggling
            MasteryData("student_B", "Algebraic Expressions", 0.35, 1),
            MasteryData("student_B", "Equations and Inequalities", 0.4, 2),
            
            # Student C: Average
            MasteryData("student_C", "Algebraic Expressions", 0.6, 2),
            MasteryData("student_C", "Functions", 0.55, 2),
        ]
        
        # Act
        gaps = analyzer.identify_critical_gaps(mastery_data)
        
        # Assert
        assert len(gaps) == 2, "Should identify gaps only for Student B"
        gap_students = [gap.student_id for gap in gaps]
        assert "student_B" in gap_students
        assert "student_A" not in gap_students
        assert "student_C" not in gap_students
    
    def test_quick_check_algebraic_expressions_function(self):
        """
        Test the quick-check helper function for Algebraic Expressions gaps.
        
        This test verifies the convenience function that allows quick assessment
        of whether a student needs intervention for a specific concept.
        
        Expected behavior:
        - Function returns BossBattleQuest when mastery < 0.5
        - Function returns None when mastery >= 0.5
        - Quest contains correct student_id and concept
        """
        # Act & Assert - below threshold
        quest = check_algebraic_expressions_gap("student_X", 0.3)
        assert quest is not None, "Should return quest for mastery < 0.5"
        assert quest.student_id == "student_X"
        assert quest.failed_concept == "Algebraic Expressions"
        assert quest.boss_name == "The Expression Guardian"
        
        # Act & Assert - above threshold
        quest = check_algebraic_expressions_gap("student_Y", 0.8)
        assert quest is None, "Should return None for mastery >= 0.5"


class TestMasteryDataValidation:
    """Test suite for MasteryData validation"""
    
    def test_mastery_data_valid_score(self):
        """Test that valid mastery scores are accepted"""
        data = MasteryData("student_1", "Algebra", 0.5)
        assert data.mastery_score == 0.5
    
    def test_mastery_data_boundary_scores(self):
        """Test boundary values for mastery scores"""
        # Test lower boundary
        data_min = MasteryData("student_1", "Algebra", 0.0)
        assert data_min.mastery_score == 0.0
        
        # Test upper boundary
        data_max = MasteryData("student_1", "Algebra", 1.0)
        assert data_max.mastery_score == 1.0
    
    def test_mastery_data_invalid_score_too_high(self):
        """Test that scores above 1.0 are rejected"""
        with pytest.raises(ValueError):
            MasteryData("student_1", "Algebra", 1.5)
    
    def test_mastery_data_invalid_score_too_low(self):
        """Test that scores below 0.0 are rejected"""
        with pytest.raises(ValueError):
            MasteryData("student_1", "Algebra", -0.1)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
