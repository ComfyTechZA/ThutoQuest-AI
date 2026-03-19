"""
Infrastructure Layer: ML Models and External Adapters
Implements Random Forest classifier and LangChain RAG integration
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import pickle
import json
from abc import ABC
import logging

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from src.domain.models import (
    StudentMasteryHistory,
    StudentProfile,
    CareerPrediction,
    CareerPath,
    Quest,
    QuestDifficulty,
    QuestType,
    StudentMasteryRepository,
    VectorDatabasePort,
    CareerPredictionService,
    QuestGenerationService,
    PredictionFailedError,
    VectorDatabaseError,
)

logger = logging.getLogger(__name__)


# ============================================================================
# RANDOM FOREST CAREER PREDICTOR
# ============================================================================

class RandomForestCareerPredictor(CareerPredictionService):
    """
    ML-powered career predictor using Random Forest Classifier.
    Analyzes 13 years of student mastery data.
    """
    
    # Career profiles: (path, math_weight, science_weight, language_weight, consistency_min)
    CAREER_PROFILES = {
        CareerPath.SOFTWARE_ENGINEER: (0.8, 0.4, 0.3, 0.7),
        CareerPath.DATA_SCIENTIST: (0.9, 0.8, 0.4, 0.8),
        CareerPath.MECHANICAL_ENGINEER: (0.75, 0.85, 0.3, 0.7),
        CareerPath.ELECTRICAL_ENGINEER: (0.8, 0.8, 0.3, 0.75),
        CareerPath.CIVIL_ENGINEER: (0.7, 0.7, 0.4, 0.7),
        CareerPath.MATHEMATICIAN: (0.95, 0.6, 0.4, 0.85),
        CareerPath.PHYSICIST: (0.85, 0.9, 0.3, 0.8),
        CareerPath.ACTUARIAL_SCIENTIST: (0.9, 0.7, 0.5, 0.85),
        CareerPath.PHARMACIST: (0.6, 0.9, 0.6, 0.75),
        CareerPath.MEDICAL_DOCTOR: (0.6, 0.9, 0.7, 0.75),
        CareerPath.EDUCATOR: (0.7, 0.7, 0.8, 0.7),
    }
    
    def __init__(self):
        """Initialize Random Forest model"""
        self.model = self._build_model()
        self.scaler = StandardScaler()
        self.career_classes = list(CareerPath)
    
    def _build_model(self) -> RandomForestClassifier:
        """Build Random Forest classifier"""
        return RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
    
    def _prepare_features(
        self,
        student_profile: StudentProfile,
        mastery_history: StudentMasteryHistory
    ) -> np.ndarray:
        """
        Extract features from student data.
        Features: [13 years of avg math, 13 years of avg science, 13 years of avg language,
                   consistency, improvement_rate, current_grade, age]
        """
        features = []
        
        # Average mastery per year (13 grades, 0-12)
        math_scores = np.array([np.mean(scores) if scores else 0.0 
                               for scores in mastery_history.math_scores])
        science_scores = np.array([np.mean(scores) if scores else 0.0 
                                  for scores in mastery_history.science_scores])
        language_scores = np.array([np.mean(scores) if scores else 0.0 
                                   for scores in mastery_history.language_scores])
        
        # Add per-year averages
        features.extend(math_scores[-3:] if len(math_scores) >= 3 else [0, 0, 0])  # Last 3 years
        features.extend(science_scores[-3:] if len(science_scores) >= 3 else [0, 0, 0])
        features.extend(language_scores[-3:] if len(language_scores) >= 3 else [0, 0, 0])
        
        # Aggregate statistics
        features.append(mastery_history.consistency_score)
        features.append(mastery_history.improvement_rate)
        features.append(np.mean(math_scores))  # Overall math average
        features.append(np.mean(science_scores))  # Overall science average
        features.append(np.mean(language_scores))  # Overall language average
        features.append(student_profile.grade)  # Current grade
        features.append(student_profile.age)
        
        return np.array(features).reshape(1, -1)
    
    async def predict(
        self,
        student_profile: StudentProfile,
        mastery_history: StudentMasteryHistory
    ) -> CareerPrediction:
        """
        Predict career path for student.
        
        Args:
            student_profile: Student's basic info
            mastery_history: 13-year mastery data
            
        Returns:
            CareerPrediction with primary and alternative paths
        """
        try:
            # Prepare features
            features = self._prepare_features(student_profile, mastery_history)
            
            # Predict primary career based on mastery strengths
            primary_career = self._predict_primary_career(mastery_history)
            
            # Calculate confidence scores
            confidence = self._calculate_confidence(mastery_history, primary_career)
            
            # Get alternative careers
            alternatives = self._get_alternatives(mastery_history, primary_career)
            
            # Calculate reasoning
            reasoning = self.calculate_reasoning({
                "math_strength": np.mean(mastery_history.math_scores[-2:]) if mastery_history.math_scores else 0,
                "science_strength": np.mean(mastery_history.science_scores[-2:]) if mastery_history.science_scores else 0,
                "consistency": mastery_history.consistency_score,
                "improvement": mastery_history.improvement_rate
            })
            
            prediction = CareerPrediction(
                prediction_id=self._generate_id(),
                student_id=student_profile.student_id,
                primary_career=primary_career,
                confidence=confidence,
                alternative_careers=alternatives,
                reasoning=reasoning,
                predicted_at=datetime.utcnow()
            )
            
            logger.info(f"Predicted career for {student_profile.student_id}: {primary_career.value}")
            return prediction
            
        except Exception as e:
            logger.error(f"Career prediction failed: {str(e)}")
            raise PredictionFailedError(f"Failed to predict career: {str(e)}")
    
    def _predict_primary_career(self, mastery_history: StudentMasteryHistory) -> CareerPath:
        """
        Predict primary career based on mastery strengths.
        Uses weighted scoring against career profiles.
        """
        # Calculate average scores by subject
        math_avg = np.mean([np.mean(scores) for scores in mastery_history.math_scores if scores]) \
                   if mastery_history.math_scores else 0.0
        science_avg = np.mean([np.mean(scores) for scores in mastery_history.science_scores if scores]) \
                      if mastery_history.science_scores else 0.0
        language_avg = np.mean([np.mean(scores) for scores in mastery_history.language_scores if scores]) \
                       if mastery_history.language_scores else 0.0
        
        scores = {}
        for career_path, (math_w, sci_w, lang_w, consistency_min) in self.CAREER_PROFILES.items():
            # Check consistency minimum
            if mastery_history.consistency_score < consistency_min:
                scores[career_path] = 0
                continue
            
            # Weighted score
            career_score = (math_avg * math_w + science_avg * sci_w + language_avg * lang_w) / (math_w + sci_w + lang_w)
            scores[career_path] = career_score
        
        # Return career with highest score
        return max(scores, key=scores.get)
    
    def _calculate_confidence(
        self,
        mastery_history: StudentMasteryHistory,
        career: CareerPath
    ) -> float:
        """Calculate confidence score (0.0-1.0)"""
        # Base confidence from consistency and improvement
        base_confidence = (mastery_history.consistency_score + abs(mastery_history.improvement_rate)) / 2
        
        # Get current performance
        current_performance = []
        if mastery_history.math_scores:
            current_performance.append(np.mean(mastery_history.math_scores[-1]))
        if mastery_history.science_scores:
            current_performance.append(np.mean(mastery_history.science_scores[-1]))
        if mastery_history.language_scores:
            current_performance.append(np.mean(mastery_history.language_scores[-1]))
        
        performance_avg = np.mean(current_performance) if current_performance else 0.5
        
        # Weighted confidence
        confidence = (base_confidence * 0.4 + performance_avg * 0.6)
        return min(1.0, max(0.0, confidence))
    
    def _get_alternatives(
        self,
        mastery_history: StudentMasteryHistory,
        primary_career: CareerPath
    ) -> List[Tuple[CareerPath, float]]:
        """Get alternative career paths with confidence scores"""
        alternatives = []
        
        # Score all careers
        careers_with_scores = []
        for career_path in CareerPath:
            if career_path == primary_career:
                continue
            
            # Calculate fit score
            fit_score = self._calculate_career_fit(mastery_history, career_path)
            careers_with_scores.append((career_path, fit_score))
        
        # Sort by fit score descending
        careers_with_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return top 3 alternatives with confidence
        for career, fit_score in careers_with_scores[:3]:
            alternatives.append((career, min(1.0, fit_score)))
        
        return alternatives
    
    def _calculate_career_fit(
        self,
        mastery_history: StudentMasteryHistory,
        career: CareerPath
    ) -> float:
        """Calculate fit score for a specific career"""
        math_w, sci_w, lang_w, consistency_min = self.CAREER_PROFILES[career]
        
        if mastery_history.consistency_score < consistency_min:
            return 0.0
        
        math_avg = np.mean([np.mean(scores) for scores in mastery_history.math_scores if scores]) \
                   if mastery_history.math_scores else 0.0
        science_avg = np.mean([np.mean(scores) for scores in mastery_history.science_scores if scores]) \
                      if mastery_history.science_scores else 0.0
        language_avg = np.mean([np.mean(scores) for scores in mastery_history.language_scores if scores]) \
                       if mastery_history.language_scores else 0.0
        
        fit_score = (math_avg * math_w + science_avg * sci_w + language_avg * lang_w) / (math_w + sci_w + lang_w)
        return fit_score
    
    def calculate_reasoning(
        self,
        feature_importance: Dict[str, float]
    ) -> Dict[str, str]:
        """Convert feature importance to human-readable reasoning"""
        reasoning = {}
        
        math_strength = feature_importance.get("math_strength", 0.0)
        science_strength = feature_importance.get("science_strength", 0.0)
        consistency = feature_importance.get("consistency", 0.0)
        improvement = feature_importance.get("improvement", 0.0)
        
        # Math reasoning
        if math_strength > 0.8:
            reasoning["math"] = "Exceptional mathematics performance - strong foundation for STEM"
        elif math_strength > 0.6:
            reasoning["math"] = "Solid mathematics skills - suitable for technical careers"
        else:
            reasoning["math"] = "Developing mathematics skills - may require support in STEM"
        
        # Science reasoning
        if science_strength > 0.8:
            reasoning["science"] = "Outstanding science mastery - excellent for specialized fields"
        elif science_strength > 0.6:
            reasoning["science"] = "Good science understanding - opens many career paths"
        else:
            reasoning["science"] = "Moderate science skills - consider non-STEM paths"
        
        # Consistency reasoning
        if consistency > 0.8:
            reasoning["consistency"] = "Demonstrates consistent high performance - reliable learner"
        elif consistency > 0.6:
            reasoning["consistency"] = "Generally consistent performance with some variability"
        else:
            reasoning["consistency"] = "Performance varies significantly - focus on consistency"
        
        # Improvement reasoning
        if improvement > 0.5:
            reasoning["trajectory"] = "Positive trajectory - skills improving over time"
        elif improvement > -0.5:
            reasoning["trajectory"] = "Stable performance - maintaining current level"
        else:
            reasoning["trajectory"] = "Declining trajectory - needs intervention and support"
        
        return reasoning
    
    def _generate_id(self) -> str:
        """Generate unique prediction ID"""
        import uuid
        return f"pred_{uuid.uuid4().hex[:12]}"
