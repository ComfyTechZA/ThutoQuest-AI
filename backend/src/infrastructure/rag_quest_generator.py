"""
LangChain RAG Integration for Quest Generation
Generates math/coding challenges from DBE textbook embeddings
"""

from typing import Dict, List, Optional
from datetime import datetime
import logging
import uuid
import json

from src.domain.models import (
    Quest,
    QuestDifficulty,
    QuestType,
    StudentProfile,
    StudentMasteryHistory,
    CareerPrediction,
    QuestGenerationService,
    VectorDatabasePort,
    QuestGenerationError,
    VectorDatabaseError,
)

logger = logging.getLogger(__name__)


# ============================================================================
# VECTOR DATABASE ADAPTER
# ============================================================================

class DBETextbookVectorDB(VectorDatabasePort):
    """
    Vector database adapter for DBE textbook content.
    Implements RAG retrieval from embeddings.
    """
    
    def __init__(self):
        """Initialize vector database adapter"""
        # In production, this would connect to actual vector store
        # (Pinecone, Weaviate, Chroma, Milvus, etc.)
        self.mock_index = self._load_mock_textbook_index()
    
    def _load_mock_textbook_index(self) -> Dict:
        """Load mock DBE textbook content index"""
        return {
            "mathematics": {
                "grade_10": [
                    {
                        "id": "math_10_001",
                        "title": "Quadratic Equations",
                        "content": "Solve x^2 - 5x + 6 = 0 using factorization",
                        "difficulty": "intermediate",
                        "concepts": ["quadratic", "factorization", "roots"],
                        "chapter": 2,
                        "source": "Grade 10 Mathematics Textbook, Chapter 2"
                    },
                    {
                        "id": "math_10_002",
                        "title": "Polynomial Operations",
                        "content": "Simplify (2x^3 - 5x^2 + 3x - 1) - (x^3 + 2x^2 - x + 4)",
                        "difficulty": "intermediate",
                        "concepts": ["polynomials", "simplification", "algebra"],
                        "chapter": 1,
                        "source": "Grade 10 Mathematics Textbook, Chapter 1"
                    },
                    {
                        "id": "math_10_003",
                        "title": "Linear Systems",
                        "content": "Solve the system: 2x + y = 7, x - y = 1",
                        "difficulty": "beginner",
                        "concepts": ["linear_systems", "substitution", "elimination"],
                        "chapter": 3,
                        "source": "Grade 10 Mathematics Textbook, Chapter 3"
                    }
                ],
                "grade_11": [
                    {
                        "id": "math_11_001",
                        "title": "Sequences and Series",
                        "content": "Find the 20th term of arithmetic sequence with a=2, d=3",
                        "difficulty": "intermediate",
                        "concepts": ["sequences", "arithmetic", "patterns"],
                        "chapter": 4,
                        "source": "Grade 11 Mathematics Textbook"
                    }
                ]
            },
            "coding": {
                "grade_10": [
                    {
                        "id": "code_10_001",
                        "title": "Python Loop Optimization",
                        "content": "Write an optimized Python function to find all prime numbers up to 100",
                        "difficulty": "intermediate",
                        "concepts": ["loops", "algorithms", "optimization"],
                        "chapter": 5,
                        "source": "DBE Computer Science Resources"
                    },
                    {
                        "id": "code_10_002",
                        "title": "Data Structure Basics",
                        "content": "Implement a stack data structure with push, pop, and peek operations",
                        "difficulty": "advanced",
                        "concepts": ["data_structures", "oop", "implementation"],
                        "chapter": 6,
                        "source": "DBE Computer Science Resources"
                    }
                ]
            }
        }
    
    async def search_content(
        self,
        query: str,
        subject: str,
        grade: int,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Search vector database for relevant content.
        
        Args:
            query: Search query string
            subject: Subject area (mathematics, coding, etc.)
            grade: Grade level (0-12)
            top_k: Number of results to return
            
        Returns:
            List of relevant content documents
        """
        try:
            # Convert grade to string key
            grade_key = f"grade_{grade}"
            
            # For mock implementation, return relevant content
            results = []
            
            if subject in self.mock_index:
                if grade_key in self.mock_index[subject]:
                    documents = self.mock_index[subject][grade_key]
                    
                    # Simple keyword matching for mock
                    scored_docs = []
                    for doc in documents:
                        score = self._calculate_relevance(query, doc)
                        scored_docs.append((doc, score))
                    
                    # Sort by score descending
                    scored_docs.sort(key=lambda x: x[1], reverse=True)
                    results = [doc for doc, _ in scored_docs[:top_k]]
            
            logger.info(f"Retrieved {len(results)} documents for {subject} grade {grade}")
            return results
            
        except Exception as e:
            logger.error(f"Vector database search failed: {str(e)}")
            raise VectorDatabaseError(f"Search failed: {str(e)}")
    
    def _calculate_relevance(self, query: str, document: Dict) -> float:
        """
        Calculate relevance score between query and document.
        In production, use embedding similarity (cosine).
        """
        query_words = set(query.lower().split())
        doc_text = (document.get("title", "") + " " + document.get("content", "")).lower()
        
        matches = sum(1 for word in query_words if word in doc_text)
        return matches / len(query_words) if query_words else 0.0


# ============================================================================
# LANGCHAIN RAG QUEST GENERATOR
# ============================================================================

class LangChainRAGQuestGenerator(QuestGenerationService):
    """
    Quest generator using LangChain and RAG.
    Retrieves content from DBE textbooks and generates personalized quests.
    """
    
    def __init__(self, vector_db: VectorDatabasePort):
        """Initialize quest generator with vector database"""
        self.vector_db = vector_db
        self.difficulty_mapping = {
            0.0: QuestDifficulty.BEGINNER,
            0.33: QuestDifficulty.BEGINNER,
            0.66: QuestDifficulty.INTERMEDIATE,
            1.0: QuestDifficulty.ADVANCED
        }
    
    async def generate_quest(
        self,
        student_id: str,
        student_profile: StudentProfile,
        mastery_history: StudentMasteryHistory,
        career_prediction: Optional[CareerPrediction] = None
    ) -> Quest:
        """
        Generate a personalized quest for student.
        
        Args:
            student_id: Student ID
            student_profile: Student profile data
            mastery_history: Student's mastery history
            career_prediction: Optional career prediction for alignment
            
        Returns:
            Generated Quest entity
        """
        try:
            # Step 1: Identify gap areas
            gap_areas = self._identify_gap_areas(mastery_history)
            
            # Step 2: Determine appropriate difficulty
            difficulty = self._calculate_difficulty(mastery_history, gap_areas)
            
            # Step 3: Select subject based on career (if available)
            subject = self._select_subject(career_prediction, gap_areas)
            
            # Step 4: Retrieve relevant content via RAG
            retrieved_content = await self.vector_db.search_content(
                query=gap_areas[0] if gap_areas else "mathematics",
                subject=subject,
                grade=student_profile.grade,
                top_k=3
            )
            
            if not retrieved_content:
                raise QuestGenerationError("No relevant content found in vector database")
            
            # Step 5: Generate quest from retrieved content
            source_doc = retrieved_content[0]
            quest = self._create_quest(
                student_id=student_id,
                source_doc=source_doc,
                difficulty=difficulty,
                subject=subject,
                student_grade=student_profile.grade
            )
            
            logger.info(f"Generated quest {quest.quest_id} for student {student_id}")
            return quest
            
        except Exception as e:
            logger.error(f"Quest generation failed: {str(e)}")
            raise QuestGenerationError(f"Failed to generate quest: {str(e)}")
    
    def _identify_gap_areas(self, mastery_history: StudentMasteryHistory) -> List[str]:
        """Identify weak areas from mastery history"""
        # Find subjects/topics with lower recent mastery scores
        gaps = []
        
        # Recent math performance
        if mastery_history.math_scores:
            recent_math = np.mean(mastery_history.math_scores[-1]) if mastery_history.math_scores[-1] else 0.5
            if recent_math < 0.7:
                gaps.append("mathematics")
        
        # Recent science performance
        if mastery_history.science_scores:
            recent_science = np.mean(mastery_history.science_scores[-1]) if mastery_history.science_scores[-1] else 0.5
            if recent_science < 0.7:
                gaps.append("science")
        
        return gaps if gaps else ["mathematics"]
    
    def _calculate_difficulty(
        self,
        mastery_history: StudentMasteryHistory,
        gap_areas: List[str]
    ) -> QuestDifficulty:
        """Determine appropriate quest difficulty"""
        # Get overall performance
        all_scores = []
        
        for scores_list in mastery_history.math_scores:
            all_scores.extend(scores_list)
        for scores_list in mastery_history.science_scores:
            all_scores.extend(scores_list)
        
        if not all_scores:
            return QuestDifficulty.BEGINNER
        
        avg_performance = np.mean(all_scores)
        
        # Difficulty based on performance
        if avg_performance > 0.8:
            return QuestDifficulty.ADVANCED
        elif avg_performance > 0.6:
            return QuestDifficulty.INTERMEDIATE
        else:
            return QuestDifficulty.BEGINNER
    
    def _select_subject(
        self,
        career_prediction: Optional[CareerPrediction],
        gap_areas: List[str]
    ) -> str:
        """Select subject based on career prediction or gaps"""
        # If career prediction suggests specific subject, prioritize it
        if career_prediction:
            from src.domain.models import CareerPath
            
            # Map careers to subjects
            career_subject_map = {
                CareerPath.SOFTWARE_ENGINEER: "coding",
                CareerPath.DATA_SCIENTIST: "mathematics",
                CareerPath.MATHEMATICIAN: "mathematics",
                CareerPath.PHYSICIST: "science",
                # Add more mappings
            }
            
            if career_prediction.primary_career in career_subject_map:
                return career_subject_map[career_prediction.primary_career]
        
        # Fall back to gap areas
        return gap_areas[0] if gap_areas else "mathematics"
    
    def _create_quest(
        self,
        student_id: str,
        source_doc: Dict,
        difficulty: QuestDifficulty,
        subject: str,
        student_grade: int
    ) -> Quest:
        """Create Quest entity from retrieved content"""
        quest_id = f"quest_{uuid.uuid4().hex[:12]}"
        
        # Determine quest type
        quest_type = QuestType.MATH_PROBLEM if subject == "mathematics" else QuestType.CODING_CHALLENGE
        
        # Generate hint based on content
        hint = self._generate_hint(source_doc)
        
        # Estimate time based on difficulty
        time_estimates = {
            QuestDifficulty.BEGINNER: 15,
            QuestDifficulty.INTERMEDIATE: 30,
            QuestDifficulty.ADVANCED: 45,
            QuestDifficulty.EXPERT: 60
        }
        
        quest = Quest(
            quest_id=quest_id,
            student_id=student_id,
            title=source_doc.get("title", "Challenge"),
            description=f"Solve this {difficulty.value} {subject} problem",
            content=source_doc.get("content", ""),
            difficulty=difficulty,
            quest_type=quest_type,
            subject=subject,
            topics=source_doc.get("concepts", []),
            source_material=source_doc.get("source", "DBE Resource"),
            estimated_time_minutes=time_estimates.get(difficulty, 30),
            points_reward=self._calculate_points(difficulty),
            solution_hint=hint,
            reference_grade=student_grade,
            generated_at=datetime.utcnow()
        )
        
        return quest
    
    def _generate_hint(self, document: Dict) -> str:
        """Generate a helpful hint from document content"""
        content = document.get("content", "")
        concepts = document.get("concepts", [])
        
        if concepts:
            hint = f"Hint: Focus on {', '.join(concepts[:2])} concepts"
        else:
            hint = "Hint: Break the problem into smaller steps"
        
        return hint
    
    def _calculate_points(self, difficulty: QuestDifficulty) -> int:
        """Calculate reward points based on difficulty"""
        points_map = {
            QuestDifficulty.BEGINNER: 100,
            QuestDifficulty.INTERMEDIATE: 250,
            QuestDifficulty.ADVANCED: 500,
            QuestDifficulty.EXPERT: 1000
        }
        return points_map.get(difficulty, 200)


# Import numpy for calculations
import numpy as np
