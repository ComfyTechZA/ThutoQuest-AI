"""
Grade 10 Critical Gaps Analysis and Quest Generation
Domain logic for identifying knowledge gaps and generating remedial quests
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class QuestType(str, Enum):
    """Types of quests available in ThutoQuest-AI"""
    NORMAL = "normal_quest"
    BOSS_BATTLE = "boss_battle"
    CHALLENGE = "challenge_quest"


class CriticalGapType(str, Enum):
    """Types of critical gaps identified"""
    FOUNDATIONAL = "foundational"
    PREREQUISITE = "prerequisite"
    CORE_CONCEPT = "core_concept"


@dataclass
class MasteryData:
    """Represents student mastery for a curriculum node"""
    student_id: str
    curriculum_node: str
    mastery_score: float
    attempts: int = 0
    
    def __post_init__(self):
        if not 0.0 <= self.mastery_score <= 1.0:
            raise ValueError("Mastery score must be between 0.0 and 1.0")


@dataclass
class CriticalGap:
    """Represents an identified critical gap"""
    student_id: str
    node_name: str
    mastery_score: float
    gap_type: CriticalGapType
    recommended_action: str
    severity: int  # 1-5 scale


@dataclass
class BossBattleQuest:
    """Represents a Boss Battle remedial quest"""
    quest_id: str
    student_id: str
    failed_concept: str
    boss_name: str
    objectives: List[str]
    reward_points: int
    difficulty: str
    description: str


class Grade10CriticalGapAnalyzer:
    """
    Analyzes Grade 10 student mastery data to identify critical gaps
    and generates remedial quests (Boss Battles) for foundational concepts.
    """
    
    # Critical threshold for identifying gaps
    CRITICAL_THRESHOLD = 0.5
    
    # Foundational concepts that require Boss Battles if below threshold
    FOUNDATIONAL_CONCEPTS = {
        "Algebraic Expressions": {
            "severity": 5,
            "gap_type": CriticalGapType.FOUNDATIONAL,
            "boss_name": "The Expression Guardian",
            "description": "Master the fundamentals of algebraic expressions"
        },
        "Equations and Inequalities": {
            "severity": 5,
            "gap_type": CriticalGapType.FOUNDATIONAL,
            "boss_name": "The Balance Keeper",
            "description": "Restore balance to mathematical equations"
        },
        "Functions": {
            "severity": 4,
            "gap_type": CriticalGapType.CORE_CONCEPT,
            "boss_name": "The Function Master",
            "description": "Unlock the power of functions"
        },
        "Graphs and Transformations": {
            "severity": 4,
            "gap_type": CriticalGapType.CORE_CONCEPT,
            "boss_name": "The Grid Mapper",
            "description": "Navigate through graphs and transformations"
        }
    }
    
    def __init__(self):
        """Initialize the Critical Gap Analyzer"""
        self.identified_gaps: List[CriticalGap] = []
        self.boss_battles: List[BossBattleQuest] = []
    
    def identify_critical_gaps(self, mastery_data_list: List[MasteryData]) -> List[CriticalGap]:
        """
        Identify critical gaps from mastery data
        
        Args:
            mastery_data_list: List of student mastery records
            
        Returns:
            List of identified critical gaps
        """
        self.identified_gaps = []
        
        for mastery in mastery_data_list:
            # Check if it's a foundational concept below threshold
            if mastery.curriculum_node in self.FOUNDATIONAL_CONCEPTS:
                if mastery.mastery_score < self.CRITICAL_THRESHOLD:
                    gap_config = self.FOUNDATIONAL_CONCEPTS[mastery.curriculum_node]
                    
                    critical_gap = CriticalGap(
                        student_id=mastery.student_id,
                        node_name=mastery.curriculum_node,
                        mastery_score=mastery.mastery_score,
                        gap_type=gap_config["gap_type"],
                        recommended_action=f"Trigger Boss Battle: {gap_config['boss_name']}",
                        severity=gap_config["severity"]
                    )
                    
                    self.identified_gaps.append(critical_gap)
        
        return self.identified_gaps
    
    def generate_boss_battle_quests(self, critical_gaps: List[CriticalGap]) -> List[BossBattleQuest]:
        """
        Generate Boss Battle quests for critical gaps
        
        Args:
            critical_gaps: List of identified critical gaps
            
        Returns:
            List of Boss Battle quests
        """
        self.boss_battles = []
        
        for gap in critical_gaps:
            if gap.node_name in self.FOUNDATIONAL_CONCEPTS:
                config = self.FOUNDATIONAL_CONCEPTS[gap.node_name]
                
                boss_battle = BossBattleQuest(
                    quest_id=f"boss_battle_{gap.student_id}_{gap.node_name.replace(' ', '_')}",
                    student_id=gap.student_id,
                    failed_concept=gap.node_name,
                    boss_name=config["boss_name"],
                    objectives=self._generate_objectives(gap.node_name),
                    reward_points=500 + (gap.severity * 100),
                    difficulty="Hard",
                    description=config["description"]
                )
                
                self.boss_battles.append(boss_battle)
        
        return self.boss_battles
    
    def _generate_objectives(self, concept: str) -> List[str]:
        """Generate learning objectives for a concept"""
        objectives_map = {
            "Algebraic Expressions": [
                "Simplify expressions with like terms",
                "Expand brackets and apply distributive property",
                "Factor algebraic expressions",
                "Manipulate and rearrange expressions"
            ],
            "Equations and Inequalities": [
                "Solve linear equations",
                "Solve quadratic equations",
                "Graph inequalities",
                "Apply equations to real-world scenarios"
            ],
            "Functions": [
                "Understand function notation",
                "Evaluate functions",
                "Determine domain and range",
                "Compose and inverse functions"
            ],
            "Graphs and Transformations": [
                "Plot points and read coordinates",
                "Translate and transform graphs",
                "Identify key features of graphs",
                "Analyze rates of change"
            ]
        }
        return objectives_map.get(concept, ["Complete remedial exercises", "Retake assessment"])
    
    def analyze_student(self, student_id: str, mastery_records: List[MasteryData]) -> dict:
        """
        Comprehensive analysis for a single student
        
        Args:
            student_id: The student's ID
            mastery_records: Student's mastery data
            
        Returns:
            Dictionary containing gaps and recommended quests
        """
        # Filter records for this student
        student_records = [m for m in mastery_records if m.student_id == student_id]
        
        # Identify gaps
        gaps = self.identify_critical_gaps(student_records)
        
        # Generate quests for gaps
        quests = self.generate_boss_battle_quests(gaps)
        
        return {
            "student_id": student_id,
            "critical_gaps": [
                {
                    "concept": gap.node_name,
                    "mastery_score": gap.mastery_score,
                    "severity": gap.severity,
                    "recommended_action": gap.recommended_action
                }
                for gap in gaps
            ],
            "boss_battle_quests": [
                {
                    "quest_id": quest.quest_id,
                    "boss_name": quest.boss_name,
                    "concept": quest.failed_concept,
                    "objectives": quest.objectives,
                    "reward_points": quest.reward_points,
                    "description": quest.description
                }
                for quest in quests
            ],
            "has_critical_gaps": len(gaps) > 0,
            "total_gaps": len(gaps)
        }
    
    def get_remedial_recommendation(self, concept: str, mastery_score: float) -> Optional[BossBattleQuest]:
        """
        Get remedial recommendation for a specific concept
        
        Args:
            concept: Curriculum concept name
            mastery_score: Student's current mastery score
            
        Returns:
            Boss Battle quest if below threshold, None otherwise
        """
        if mastery_score >= self.CRITICAL_THRESHOLD:
            return None
        
        if concept not in self.FOUNDATIONAL_CONCEPTS:
            return None
        
        config = self.FOUNDATIONAL_CONCEPTS[concept]
        
        boss_battle = BossBattleQuest(
            quest_id=f"boss_battle_{concept.replace(' ', '_')}",
            student_id="temp_student",  # To be set by application
            failed_concept=concept,
            boss_name=config["boss_name"],
            objectives=self._generate_objectives(concept),
            reward_points=500 + (config["severity"] * 100),
            difficulty="Hard",
            description=config["description"]
        )
        
        return boss_battle


# Example usage and helper function
def check_algebraic_expressions_gap(student_id: str, mastery_score: float) -> Optional[BossBattleQuest]:
    """
    Quick check for Algebraic Expressions critical gap
    Returns a Boss Battle quest if mastery is below 0.5
    
    Args:
        student_id: Student's ID
        mastery_score: Current mastery score for Algebraic Expressions
        
    Returns:
        BossBattleQuest if gap exists, None otherwise
    """
    analyzer = Grade10CriticalGapAnalyzer()
    
    if mastery_score < analyzer.CRITICAL_THRESHOLD:
        quest = analyzer.get_remedial_recommendation("Algebraic Expressions", mastery_score)
        if quest:
            quest.student_id = student_id
        return quest
    
    return None
