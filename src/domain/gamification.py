"""
Gamification Models: Achievements, Badges, and Leaderboards
SQLAlchemy ORM models for Phase 2 gamification features
"""

from dataclasses import dataclass
from typing import List, Optional, Dict
from enum import Enum
from uuid import UUID
import json


class AchievementRarity(str, Enum):
    """Achievement rarity levels"""
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"


class LeaderboardType(str, Enum):
    """Types of leaderboards"""
    SUBJECT = "subject"
    SCHOOL = "school"
    NATIONAL = "national"
    SKILL = "skill"


class LeaderboardPeriod(str, Enum):
    """Leaderboard time periods"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ALL_TIME = "all_time"


# ============================================================================
# ACHIEVEMENT SYSTEM
# ============================================================================

@dataclass
class Achievement:
    """Represents a single achievement/badge"""
    id: UUID
    achievement_key: str  # e.g., 'math_wizard', 'perseverance_hero'
    name: str  # e.g., "Math Wizard"
    description: str
    icon_url: str
    rarity: AchievementRarity
    unlock_condition: Dict  # JSON dict defining unlock logic
    points_reward: int
    created_at: str


class AchievementUnlockCondition:
    """Defines when an achievement is unlocked"""
    
    @staticmethod
    def mastery_threshold(concept: str, threshold: float = 0.9) -> Dict:
        """Unlock when student reaches mastery threshold on a concept"""
        return {
            "type": "mastery_threshold",
            "concept": concept,
            "threshold": threshold
        }
    
    @staticmethod
    def consecutive_success(consecutive_correct: int = 5) -> Dict:
        """Unlock after N consecutive correct answers"""
        return {
            "type": "consecutive_success",
            "consecutive_correct": consecutive_correct
        }
    
    @staticmethod
    def attempts_perseverance(attempts: int = 10) -> Dict:
        """Unlock after N attempts without giving up"""
        return {
            "type": "attempts_perseverance",
            "attempts": attempts
        }
    
    @staticmethod
    def time_investment(hours: int = 10) -> Dict:
        """Unlock after spending N hours on platform"""
        return {
            "type": "time_investment",
            "hours": hours
        }
    
    @staticmethod
    def milestone_achievement(previous_achievement: str) -> Dict:
        """Unlock after achieving another achievement"""
        return {
            "type": "milestone_achievement",
            "previous_achievement": previous_achievement
        }
    
    @staticmethod
    def group_collaboration(group_members: int = 3) -> Dict:
        """Unlock when collaborating with N students"""
        return {
            "type": "group_collaboration",
            "group_members": group_members
        }


# Pre-defined achievements
ACHIEVEMENT_DEFINITIONS = {
    "math_wizard": {
        "name": "Math Wizard",
        "description": "Master all Mathematics topics",
        "icon": "🧙‍♂️",
        "rarity": AchievementRarity.EPIC,
        "points": 500,
        "unlock": AchievementUnlockCondition.mastery_threshold("Mathematics", 0.9)
    },
    "science_scholar": {
        "name": "Science Scholar",
        "description": "Achieve mastery in all Science concepts",
        "icon": "👨‍🔬",
        "rarity": AchievementRarity.EPIC,
        "points": 500,
        "unlock": AchievementUnlockCondition.mastery_threshold("Science", 0.9)
    },
    "persistence_champion": {
        "name": "Persistence Champion",
        "description": "Attempt 50+ questions without quitting",
        "icon": "💪",
        "rarity": AchievementRarity.RARE,
        "points": 300,
        "unlock": AchievementUnlockCondition.attempts_perseverance(50)
    },
    "accuracy_ace": {
        "name": "Accuracy Ace",
        "description": "Get 10 consecutive correct answers",
        "icon": "🎯",
        "rarity": AchievementRarity.RARE,
        "points": 250,
        "unlock": AchievementUnlockCondition.consecutive_success(10)
    },
    "dedicated_learner": {
        "name": "Dedicated Learner",
        "description": "Spend 50+ hours on ThutoQuest-AI",
        "icon": "📚",
        "rarity": AchievementRarity.UNCOMMON,
        "points": 200,
        "unlock": AchievementUnlockCondition.time_investment(50)
    },
    "team_player": {
        "name": "Team Player",
        "description": "Join a study group and collaborate",
        "icon": "🤝",
        "rarity": AchievementRarity.UNCOMMON,
        "points": 150,
        "unlock": AchievementUnlockCondition.group_collaboration(1)
    },
    "speed_demon": {
        "name": "Speed Demon",
        "description": "Complete 5 quizzes in one day",
        "icon": "⚡",
        "rarity": AchievementRarity.COMMON,
        "points": 100,
        "unlock": {"type": "daily_quiz_count", "count": 5}
    },
    "comeback_kid": {
        "name": "Comeback Kid",
        "description": "Improve from 0.3 to 0.8 mastery score",
        "icon": "🔥",
        "rarity": AchievementRarity.RARE,
        "points": 300,
        "unlock": {"type": "score_improvement", "from": 0.3, "to": 0.8}
    },
    "week_warrior": {
        "name": "Week Warrior",
        "description": "Maintain activity for 7 consecutive days",
        "icon": "⚔️",
        "rarity": AchievementRarity.UNCOMMON,
        "points": 180,
        "unlock": {"type": "consecutive_days", "days": 7}
    },
    "jack_of_all_trades": {
        "name": "Jack of All Trades",
        "description": "Master topics from 5+ subjects",
        "icon": "🎭",
        "rarity": AchievementRarity.RARE,
        "points": 350,
        "unlock": {"type": "multi_subject_mastery", "subjects": 5}
    }
}


@dataclass
class StudentAchievement:
    """Represents an achievement earned by a student"""
    id: UUID
    student_id: UUID
    achievement_id: UUID
    achievement_key: str
    unlocked_at: str


# ============================================================================
# LEADERBOARD SYSTEM
# ============================================================================

@dataclass
class LeaderboardEntry:
    """Represents a student's position on a leaderboard"""
    rank: int
    student_id: UUID
    student_name: str
    school: str
    points: int
    mastery_score: float
    achievements_earned: int
    status: str  # 'active', 'inactive', 'new'


@dataclass
class LeaderboardResult:
    """Complete leaderboard response"""
    type: LeaderboardType
    period: LeaderboardPeriod
    generated_at: str
    total_participants: int
    entries: List[LeaderboardEntry]


class LeaderboardCalculator:
    """Calculate student rankings and scores"""
    
    SCORE_WEIGHTS = {
        "mastery": 0.50,           # 50% - Average mastery score
        "achievements": 0.20,       # 20% - Achievement count
        "engagement": 0.15,         # 15% - Time on task
        "improvement": 0.15         # 15% - Recent improvement
    }
    
    @staticmethod
    def calculate_leaderboard_score(
        mastery_score: float,
        achievement_count: int,
        time_on_task_hours: int,
        improvement_rate: float,
        max_achievements: int = 50
    ) -> int:
        """
        Calculate composite leaderboard score.
        
        Args:
            mastery_score: Average mastery (0.0-1.0)
            achievement_count: Number of achievements unlocked
            time_on_task_hours: Total hours spent
            improvement_rate: Recent improvement (slope of mastery over time)
            max_achievements: Max possible achievements
        
        Returns:
            Composite score (0-10000)
        """
        # Normalize components to 0-1 scale
        mastery_norm = mastery_score  # Already 0-1
        achievement_norm = min(achievement_count / max_achievements, 1.0)
        engagement_norm = min(time_on_task_hours / 100, 1.0)  # 100 hrs = max
        improvement_norm = min(max(improvement_rate, 0), 1.0)  # Cap at 100% improvement
        
        # Calculate weighted score
        weighted_score = (
            (mastery_norm * LeaderboardCalculator.SCORE_WEIGHTS["mastery"]) +
            (achievement_norm * LeaderboardCalculator.SCORE_WEIGHTS["achievements"]) +
            (engagement_norm * LeaderboardCalculator.SCORE_WEIGHTS["engagement"]) +
            (improvement_norm * LeaderboardCalculator.SCORE_WEIGHTS["improvement"])
        )
        
        # Scale to 0-10000
        return int(weighted_score * 10000)
    
    @staticmethod
    def rank_students(scores: List[tuple]) -> List[LeaderboardEntry]:
        """
        Rank students by score.
        
        Args:
            scores: List of (student_id, student_name, school, score, mastery, achievements)
        
        Returns:
            Ranked list of LeaderboardEntry objects
        """
        # Sort by score descending
        sorted_scores = sorted(scores, key=lambda x: x[3], reverse=True)
        
        entries = []
        for rank, (student_id, name, school, score, mastery, achievements) in enumerate(sorted_scores, 1):
            entries.append(LeaderboardEntry(
                rank=rank,
                student_id=student_id,
                student_name=name,
                school=school,
                points=score,
                mastery_score=mastery,
                achievements_earned=achievements,
                status="active"
            ))
        
        return entries
    
    @staticmethod
    def rank_by_subject(
        scores: List[tuple],
        subject: str
    ) -> List[LeaderboardEntry]:
        """Rank students specifically for a subject"""
        return LeaderboardCalculator.rank_students(scores)


class AchievementUnlocker:
    """Business logic for unlocking achievements"""
    
    @staticmethod
    def check_mastery_threshold(
        student_id: str,
        concept: str,
        current_mastery: float,
        achievement_key: str
    ) -> bool:
        """Check if student unlocked achievement via mastery threshold"""
        achievement = ACHIEVEMENT_DEFINITIONS.get(achievement_key)
        if not achievement:
            return False
        
        unlock_condition = achievement["unlock"]
        if unlock_condition.get("type") != "mastery_threshold":
            return False
        
        threshold = unlock_condition.get("threshold", 0.8)
        return current_mastery >= threshold
    
    @staticmethod
    def check_consecutive_success(
        correct_count: int,
        achievement_key: str = "accuracy_ace"
    ) -> bool:
        """Check if student unlocked achievement via consecutive correct answers"""
        achievement = ACHIEVEMENT_DEFINITIONS.get(achievement_key)
        if not achievement:
            return False
        
        unlock_condition = achievement["unlock"]
        if unlock_condition.get("type") != "consecutive_success":
            return False
        
        required = unlock_condition.get("consecutive_correct", 10)
        return correct_count >= required
    
    @staticmethod
    def check_perseverance(
        attempts: int,
        achievement_key: str = "persistence_champion"
    ) -> bool:
        """Check if student unlocked perseverance achievement"""
        achievement = ACHIEVEMENT_DEFINITIONS.get(achievement_key)
        if not achievement:
            return False
        
        unlock_condition = achievement["unlock"]
        if unlock_condition.get("type") != "attempts_perseverance":
            return False
        
        required = unlock_condition.get("attempts", 50)
        return attempts >= required
    
    @staticmethod
    def get_unlockable_achievements(
        mastery_score: float,
        attempt_count: int,
        achievement_count: int,
        hours_spent: float
    ) -> List[str]:
        """
        Get list of achievements that can be unlocked given current stats.
        
        Returns:
            List of achievement keys that can be unlocked
        """
        unlockable = []
        
        if mastery_score >= 0.9 and "math_wizard" not in [a for a in range(achievement_count)]:
            unlockable.append("math_wizard")
        
        if attempt_count >= 10 and "accuracy_ace" not in unlockable:
            unlockable.append("accuracy_ace")
        
        if attempt_count >= 50 and "persistence_champion" not in unlockable:
            unlockable.append("persistence_champion")
        
        if hours_spent >= 50 and "dedicated_learner" not in unlockable:
            unlockable.append("dedicated_learner")
        
        return unlockable


# ============================================================================
# GAMIFICATION METRICS
# ============================================================================

@dataclass
class StudentGamificationProfile:
    """Complete gamification profile for a student"""
    student_id: UUID
    total_points: int
    achievement_count: int
    leaderboard_ranks: Dict[str, int]  # type -> current rank
    current_streak: int  # consecutive days active
    total_hours_spent: float
    total_attempts: int
    achievements: List[StudentAchievement]
    recent_achievements: List[StudentAchievement]  # Last 5
    
    def get_engagement_level(self) -> str:
        """Determine engagement level"""
        if self.total_hours_spent >= 50:
            return "Dedicated"
        elif self.total_hours_spent >= 25:
            return "Regular"
        elif self.total_hours_spent >= 5:
            return "Casual"
        else:
            return "New"
    
    def get_level(self) -> int:
        """Calculate player level based on points"""
        # 1000 points per level
        return max(1, self.total_points // 1000)
    
    def get_next_level_progress(self) -> float:
        """Get progress to next level (0.0-1.0)"""
        current_level = self.get_level()
        points_for_level = current_level * 1000
        points_for_next = (current_level + 1) * 1000
        progress = (self.total_points - points_for_level) / (points_for_next - points_for_level)
        return min(1.0, max(0.0, progress))
