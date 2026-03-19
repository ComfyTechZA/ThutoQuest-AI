"""
Mock Data Generator for ThutoQuest-AI
Generates 50 Grade 10 students with varying mastery scores in Math and Science
for testing and demonstrating the AI intervention logic
"""

import json
import csv
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from dataclasses import asdict

# Import domain logic (for critical gap analysis)
import sys
sys.path.insert(0, '../')
from src.domain.grade10_logic import (
    Grade10CriticalGapAnalyzer,
    MasteryData,
    CriticalGapType
)


class MockDataGenerator:
    """Generates realistic mock data for Grade 10 students and mastery tracking"""
    
    # Sample names for students
    FIRST_NAMES = [
        "Amuhle", "Thandi", "Sipho", "Naledi", "Kayla",
        "Mandla", "Tebogo", "Nandi", "Lucas", "Precious",
        "Bongani", "Kopano", "Lerato", "Zola", "Ofentse",
        "Thapelo", "Thembi", "Mpumelelo", "Siyanda", "Zanele",
        "Ayanda", "Khethiwe", "Sifiso", "Nomsa", "Thabo",
        "Busisiwe", "Tendai", "Mpho", "Lindiwe", "Vusi",
        "Nkosikhona", "Sizwe", "Anele", "Kabelo", "Thandeka",
        "Lungile", "Sandile", "Nomcebo", "Sibusiso", "Themba",
        "Noxolo", "Dlamini", "Mokgadi", "Tumi", "Kamogelo",
        "Khanyi", "Senzo", "Ntombifuthi", "Fiona", "Karim"
    ]
    
    LAST_NAMES = [
        "Mkhize", "Ndlela", "Dlamini", "Khumalo", "Ngcobo",
        "Mthembu", "Nkosi", "Sithole", "Mhlongo", "Mthiyane",
        "Jele", "Mahlobo", "Ndaba", "Gumede", "Zwane",
        "Madlala", "Khumalo", "Ndlela", "Mkhaya", "Sibanda"
    ]
    
    SCHOOLS = [
        "Northwich Academy",
        "St. John's College",
        "Sandton High School",
        "Roodepoort High",
        "Bryanston School",
        "Berea Park High",
        "Parktown High",
        "Waterford Valley",
        "Ridgeway School",
        "Sunridge Park"
    ]
    
    # Grade 10 Curriculum Nodes
    MATH_TOPICS = [
        "Algebraic Expressions",
        "Equations and Inequalities",
        "Functions",
        "Graphs and Transformations",
        "Coordinate Geometry",
        "Trigonometry",
        "Statistics and Probability",
        "Polynomials and Factorization"
    ]
    
    SCIENCE_TOPICS = [
        "Chemical Bonding",
        "Reactions and Equations",
        "States of Matter",
        "Energy and Work",
        "Forces and Motion",
        "Waves and Sound",
        "Electricity and Magnetism",
        "Life Processes"
    ]
    
    def __init__(self, num_students: int = 50):
        """Initialize the mock data generator.
        
        Sets up internal state for generating Grade 10 student mastery tracking data.
        Creates an instance of the critical gap analyzer for identifying intervention
        opportunities.
        
        Args:
            num_students (int, optional): Number of students to generate. Defaults to 50.
                Must be a positive integer.
        
        Raises:
            ValueError: If num_students is not positive.
        
        Example:
            >>> generator = MockDataGenerator(num_students=100)
            >>> generator.generate_students()
        """
        self.num_students = num_students
        self.students = []
        self.curriculum_nodes = []
        self.mastery_records = []
        self.analyzer = Grade10CriticalGapAnalyzer()
    
    def generate_student_id(self) -> str:
        """Generate a realistic South African national identification number.
        
        Creates a valid-format South African national ID based on realistic 
        birth years (2006-2009) for Grade 10 students. Format follows the pattern:
        YYMMDDGGGGGGG where GGG represents gender and GGGG is a sequence number.
        
        Returns:
            str: A 13-digit national ID string in the format YYMMDDGGGGGGG.
        
        Example:
            >>> generator = MockDataGenerator()
            >>> nid = generator.generate_student_id()
            >>> len(nid)
            13
        """
        # Format: YYMMDDGGGGGGG (GGG = gender, GGGG = sequence)
        year = random.randint(2006, 2009)  # Grade 10 students born 2006-2009
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        gender = random.randint(4001, 4999)  # Female: 4xxx, Male: 5xxx
        sequence = random.randint(1, 9999)
        
        national_id = f"{year:02d}{month:02d}{day:02d}{gender:06d}{sequence:04d}"
        return national_id
    
    def generate_students(self) -> List[Dict]:
        """Generate mock Grade 10 student records with realistic attributes.
        
        Creates a list of student dictionaries with realistic South African names,
        national IDs, emails, school assignments, and enrollment dates. The number
        of students generated is determined by self.num_students.
        
        Returns:
            List[Dict]: A list of student dictionaries, each containing:
                - id (str): UUID for the student
                - national_id (str): SA national ID
                - first_name (str): Student's first name
                - last_name (str): Student's last name
                - email (str): Student email address
                - grade_level (int): Always 10 for Grade 10
                - school_name (str): Name of school
                - enrollment_date (str): ISO format enrollment date
                - is_active (bool): Active status flag
        
        Example:
            >>> generator = MockDataGenerator(num_students=5)
            >>> students = generator.generate_students()
            >>> len(students)
            5
            >>> 'national_id' in students[0]
            True
        """
        self.students = []
        base_date = datetime.now() - timedelta(days=365)
        
        for i in range(self.num_students):
            first_name = random.choice(self.FIRST_NAMES)
            last_name = random.choice(self.LAST_NAMES)
            
            student = {
                "id": str(uuid.uuid4()),
                "national_id": self.generate_student_id(),
                "first_name": first_name,
                "last_name": last_name,
                "email": f"{first_name.lower()}.{last_name.lower()}{i}@student.edu.za",
                "grade_level": 10,
                "school_name": random.choice(self.SCHOOLS),
                "enrollment_date": (base_date + timedelta(days=random.randint(0, 365))).isoformat(),
                "is_active": True
            }
            self.students.append(student)
        
        return self.students
    
    def generate_curriculum_nodes(self) -> List[Dict]:
        """Generate Grade 10 curriculum node records for Mathematics and Science.
        
        Creates standardized curriculum nodes representing Grade 10 learning topics.
        Includes 8 Mathematics topics and 8 Science topics with metadata like
        difficulty level, estimated hours, and descriptions.
        
        Returns:
            List[Dict]: A list of curriculum node dictionaries, each containing:
                - id (str): UUID for the curriculum node
                - subject (str): Either 'Mathematics' or 'Science'
                - topic_name (str): Name of the topic
                - grade_level (int): Always 10
                - difficulty_level (str): 'Easy', 'Medium', or 'Hard'
                - estimated_hours (int): Estimated teaching hours (8-20)
                - description (str): Brief topic description
                - sort_order (int): Display sequence number
        
        Example:
            >>> generator = MockDataGenerator()
            >>> nodes = generator.generate_curriculum_nodes()
            >>> len(nodes)
            16
            >>> sum(1 for n in nodes if n['subject'] == 'Mathematics')
            8
        """
        self.curriculum_nodes = []
        
        # Math nodes
        for idx, topic in enumerate(self.MATH_TOPICS):
            node = {
                "id": str(uuid.uuid4()),
                "subject": "Mathematics",
                "topic_name": topic,
                "grade_level": 10,
                "difficulty_level": random.choice(["Easy", "Medium", "Hard"]),
                "estimated_hours": random.randint(8, 20),
                "description": f"Grade 10 Mathematics: {topic}",
                "sort_order": idx
            }
            self.curriculum_nodes.append(node)
        
        # Science nodes
        for idx, topic in enumerate(self.SCIENCE_TOPICS):
            node = {
                "id": str(uuid.uuid4()),
                "subject": "Science",
                "topic_name": topic,
                "grade_level": 10,
                "difficulty_level": random.choice(["Easy", "Medium", "Hard"]),
                "estimated_hours": random.randint(8, 20),
                "description": f"Grade 10 Science: {topic}",
                "sort_order": idx
            }
            self.curriculum_nodes.append(node)
        
        return self.curriculum_nodes
    
    def generate_mastery_scores(self) -> List[Dict]:
        """Generate realistic mastery scores for all students across all curriculum nodes.
        
        Creates mastery records representing student performance on each curriculum
        node. Varies performance based on randomly assigned student profiles
        (high achiever, subject-specific strength, struggling, or inconsistent).
        
        Returns:
            List[Dict]: A list of mastery record dictionaries, each containing:
                - id (str): UUID for the record
                - student_id (str): Reference to student
                - curriculum_node_id (str): Reference to curriculum node
                - curriculum_node (str): Topic name
                - subject (str): Subject name
                - mastery_score (float): Score 0.0-1.0
                - number_of_attempts (int): Attempt count (1-5)
                - time_spent_minutes (int): Time invested (30-300 min)
                - last_assessment_date (str): ISO format date
                - is_mastered (bool): True if score >= 0.8
                - status (str): 'Not Started', 'In Progress', or 'Mastered'
        
        Example:
            >>> generator = MockDataGenerator(num_students=2)
            >>> generator.generate_students()
            >>> generator.generate_curriculum_nodes()
            >>> records = generator.generate_mastery_scores()
            >>> len(records)
            32  # 2 students × 16 topics
        """
        self.mastery_records = []
        
        for student in self.students:
            student_id = student["id"]
            
            # Create variation in student performance
            # Some students are strong overall, some struggle, some have specific weak areas
            performance_profile = random.choice([
                "high_achiever",      # Strong across both subjects
                "science_strong",     # Good at science, weaker at math
                "math_strong",        # Good at math, weaker at science
                "struggling",         # Below average in both
                "inconsistent"        # Mixed performance
            ])
            
            for node in self.curriculum_nodes:
                mastery_score = self._generate_score_by_profile(
                    performance_profile,
                    node["subject"],
                    node["topic_name"]
                )
                
                attempts = random.randint(1, 5)
                
                mastery_record = {
                    "id": str(uuid.uuid4()),
                    "student_id": student_id,
                    "curriculum_node_id": node["id"],
                    "curriculum_node": node["topic_name"],
                    "subject": node["subject"],
                    "mastery_score": round(mastery_score, 2),
                    "number_of_attempts": attempts,
                    "time_spent_minutes": random.randint(30, 300),
                    "last_assessment_date": (datetime.now() - timedelta(days=random.randint(1, 60))).isoformat(),
                    "is_mastered": mastery_score >= 0.8,
                    "status": self._get_status(mastery_score)
                }
                self.mastery_records.append(mastery_record)
        
        return self.mastery_records
    
    def _generate_score_by_profile(self, profile: str, subject: str, topic: str) -> float:
        """Generate a realistic mastery score based on student performance profile.
        
        Applies profile-specific score distributions and topic-specific adjustments
        to create varied, believable student performance patterns.
        
        Args:
            profile (str): Student performance profile. One of:
                - 'high_achiever': Scores 0.75-1.0 across all subjects
                - 'science_strong': Scores 0.7-0.95 Science, 0.3-0.65 Math
                - 'math_strong': Scores 0.7-0.95 Math, 0.3-0.65 Science
                - 'struggling': Scores 0.1-0.55 across all subjects
                - 'inconsistent': Scores 0.2-0.8 with random variation
            subject (str): The subject ('Mathematics' or 'Science')
            topic (str): The specific topic name for difficulty adjustment
        
        Returns:
            float: A mastery score between 0.0 and 1.0 (inclusive).
        
        Example:
            >>> generator = MockDataGenerator()
            >>> score = generator._generate_score_by_profile('high_achiever', 'Mathematics', 'Algebra')
            >>> 0.75 <= score <= 1.0
            True
        """
        base_score = 0.5
        
        if profile == "high_achiever":
            base_score = random.uniform(0.75, 1.0)
        elif profile == "science_strong":
            if subject == "Science":
                base_score = random.uniform(0.7, 0.95)
            else:
                base_score = random.uniform(0.3, 0.65)
        elif profile == "math_strong":
            if subject == "Mathematics":
                base_score = random.uniform(0.7, 0.95)
            else:
                base_score = random.uniform(0.3, 0.65)
        elif profile == "struggling":
            base_score = random.uniform(0.1, 0.55)
        elif profile == "inconsistent":
            base_score = random.uniform(0.2, 0.8)
        
        # Add variation: some topics are always harder
        if topic in ["Trigonometry", "Polynomials and Factorization", "Higher-order thinking"]:
            base_score *= 0.9
        
        # Clamp between 0.0 and 1.0
        return max(0.0, min(1.0, base_score))
    
    def _get_status(self, score: float) -> str:
        """Determine student mastery status based on score threshold.
        
        Maps numeric mastery scores to categorical status labels for easier
        interpretation and reporting.
        
        Args:
            score (float): Mastery score between 0.0 and 1.0
        
        Returns:
            str: One of:
                - 'Mastered' if score >= 0.8
                - 'In Progress' if 0.5 <= score < 0.8
                - 'Not Started' if score < 0.5
        
        Example:
            >>> generator = MockDataGenerator()
            >>> generator._get_status(0.85)
            'Mastered'
            >>> generator._get_status(0.65)
            'In Progress'
        """
        if score >= 0.8:
            return "Mastered"
        elif score >= 0.5:
            return "In Progress"
        else:
            return "Not Started"
    
    def identify_critical_gaps(self) -> Dict:
        """Analyze mastery data to identify critical gaps and generate interventions.
        
        Uses the Grade10CriticalGapAnalyzer to identify students with foundational
        concept gaps (mastery < 0.5) and generates Boss Battle remedial quests
        for them. Produces a comprehensive analysis report.
        
        Returns:
            Dict: Analysis report containing:
                - total_students (int): Total students analyzed
                - students_with_gaps (List[Dict]): Students needing intervention with:
                    - student_id, student_name, national_id
                    - gaps: List of identified gaps
                    - boss_battles: List of recommended quest interventions
                - gap_summary (Dict): Concept name -> count of students with gap
        
        Raises:
            RuntimeError: If mastery records haven't been generated yet.
        
        Example:
            >>> generator = MockDataGenerator(num_students=10)
            >>> generator.generate_students()
            >>> generator.generate_curriculum_nodes()
            >>> generator.generate_mastery_scores()
            >>> analysis = generator.identify_critical_gaps()
            >>> 'students_with_gaps' in analysis
            True
        """
        critical_gap_analysis = {
            "total_students": len(self.students),
            "students_with_gaps": [],
            "gap_summary": {}
        }
        
        for student in self.students:
            student_mastery = [
                MasteryData(
                    student_id=record["student_id"],
                    curriculum_node=record["curriculum_node"],
                    mastery_score=record["mastery_score"]
                )
                for record in self.mastery_records
                if record["student_id"] == student["id"]
            ]
            
            analysis = self.analyzer.analyze_student(student["id"], student_mastery)
            
            if analysis["has_critical_gaps"]:
                critical_gap_analysis["students_with_gaps"].append({
                    "student_id": student["id"],
                    "student_name": f"{student['first_name']} {student['last_name']}",
                    "national_id": student["national_id"],
                    "gaps": analysis["critical_gaps"],
                    "boss_battles": analysis["boss_battle_quests"]
                })
                
                # Track gap concepts
                for gap in analysis["critical_gaps"]:
                    concept = gap["concept"]
                    if concept not in critical_gap_analysis["gap_summary"]:
                        critical_gap_analysis["gap_summary"][concept] = 0
                    critical_gap_analysis["gap_summary"][concept] += 1
        
        return critical_gap_analysis
    
    def export_to_json(self, filename: str = "mock_data.json") -> str:
        """Export all generated data to a JSON file.
        
        Serializes students, curriculum nodes, and mastery records to JSON format
        for integration with external systems or for archival purposes.
        
        Args:
            filename (str, optional): Output filename. Defaults to 'mock_data.json'.
        
        Returns:
            str: The filename that was written.
        
        Raises:
            IOError: If the file cannot be written due to permission or path issues.
        
        Example:
            >>> generator = MockDataGenerator()
            >>> generator.generate_students()
            >>> generator.generate_curriculum_nodes()
            >>> generator.generate_mastery_scores()
            >>> outfile = generator.export_to_json('output.json')
            >>> import os; os.path.exists(outfile)
            True
        """
        data = {
            "students": self.students,
            "curriculum_nodes": self.curriculum_nodes,
            "mastery_records": self.mastery_records,
            "generated_at": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Exported {len(self.students)} students to {filename}")
        return filename
    
    def export_students_csv(self, filename: str = "mock_students.csv") -> None:
        """Export student records to a CSV file.
        
        Writes student data in comma-separated values format for easy import
        into spreadsheet applications or data analysis tools.
        
        Args:
            filename (str, optional): Output CSV filename. Defaults to 'mock_students.csv'.
        
        Returns:
            None
        
        Raises:
            IOError: If the file cannot be written.
            RuntimeError: If no students have been generated yet.
        
        Example:
            >>> generator = MockDataGenerator()
            >>> generator.generate_students()
            >>> generator.export_students_csv('students.csv')
        """
        if not self.students:
            print("No students to export. Generate students first.")
            return
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.students[0].keys())
            writer.writeheader()
            writer.writerows(self.students)
        
        print(f"✓ Exported {len(self.students)} students to {filename}")
    
    def export_mastery_csv(self, filename: str = "mock_mastery.csv") -> None:
        """Export mastery assessment records to a CSV file.
        
        Writes complete mastery data including scores, attempts, and timestamps
        in CSV format for data analysis and database import.
        
        Args:
            filename (str, optional): Output CSV filename. Defaults to 'mock_mastery.csv'.
        
        Returns:
            None
        
        Raises:
            IOError: If the file cannot be written.
            RuntimeError: If no mastery records have been generated yet.
        
        Example:
            >>> generator = MockDataGenerator()
            >>> generator.generate_students()
            >>> generator.generate_curriculum_nodes()
            >>> generator.generate_mastery_scores()
            >>> generator.export_mastery_csv('mastery_data.csv')
        """
        if not self.mastery_records:
            print("No mastery records to export. Generate mastery scores first.")
            return
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.mastery_records[0].keys())
            writer.writeheader()
            writer.writerows(self.mastery_records)
        
        print(f"✓ Exported {len(self.mastery_records)} mastery records to {filename}")
    
    def print_summary(self) -> None:
        """Print a formatted summary of generated data statistics.
        
        Displays comprehensive statistics including:
        - Student and curriculum node counts
        - Mastery distribution percentages
        - Average mastery scores
        - Status breakdown (Mastered/In Progress/Not Started)
        
        Returns:
            None
        
        Example:
            >>> generator = MockDataGenerator()
            >>> generator.generate_students()
            >>> generator.generate_curriculum_nodes()
            >>> generator.generate_mastery_scores()
            >>> generator.print_summary()  # Outputs formatted statistics
        """
        print("\n" + "="*60)
        print("THUTOQUEST-AI MOCK DATA GENERATION SUMMARY")
        print("="*60)
        print(f"Students Generated: {len(self.students)}")
        print(f"Curriculum Nodes: {len(self.curriculum_nodes)}")
        print(f"  - Mathematics Topics: {len(self.MATH_TOPICS)}")
        print(f"  - Science Topics: {len(self.SCIENCE_TOPICS)}")
        print(f"Total Mastery Records: {len(self.mastery_records)}")
        
        # Calculate statistics
        avg_scores = []
        mastered = 0
        in_progress = 0
        not_started = 0
        
        for record in self.mastery_records:
            avg_scores.append(record["mastery_score"])
            if record["is_mastered"]:
                mastered += 1
            elif record["status"] == "In Progress":
                in_progress += 1
            else:
                not_started += 1
        
        print(f"\nMastery Statistics:")
        print(f"  Average Mastery Score: {sum(avg_scores)/len(avg_scores):.2f}")
        print(f"  Mastered: {mastered} ({100*mastered/len(self.mastery_records):.1f}%)")
        print(f"  In Progress: {in_progress} ({100*in_progress/len(self.mastery_records):.1f}%)")
        print(f"  Not Started: {not_started} ({100*not_started/len(self.mastery_records):.1f}%)")
        print("="*60 + "\n")
    
    def print_critical_gaps_report(self) -> None:
        """Print a formatted report of identified critical gaps and interventions.
        
        Displays a detailed analysis including:
        - Number of students requiring intervention
        - Problem areas and affected student counts
        - Sample student interventions with Boss Battle recommendations
        
        Returns:
            None
        
        Example:
            >>> generator = MockDataGenerator()
            >>> generator.generate_students()
            >>> generator.generate_curriculum_nodes()
            >>> generator.generate_mastery_scores()
            >>> generator.print_critical_gaps_report()  # Outputs gap analysis
        """
        analysis = self.identify_critical_gaps()
        
        print("\n" + "="*60)
        print("CRITICAL GAPS & BOSS BATTLE RECOMMENDATIONS")
        print("="*60)
        print(f"\nStudents Requiring Intervention: {len(analysis['students_with_gaps'])}/{analysis['total_students']}")
        
        if analysis["gap_summary"]:
            print(f"\nTop Problem Areas:")
            for concept, count in sorted(analysis["gap_summary"].items(), key=lambda x: x[1], reverse=True):
                print(f"  • {concept}: {count} students need remediation")
        
        print(f"\nSample Interventions (showing first 5):")
        for i, student_gap in enumerate(analysis["students_with_gaps"][:5]):
            print(f"\n  {i+1}. {student_gap['student_name']} (ID: {student_gap['national_id']})")
            for boss_battle in student_gap["boss_battles"]:
                print(f"     🎯 {boss_battle['boss_name']}")
                print(f"        Concept: {boss_battle['concept']}")
                print(f"        Reward: {boss_battle['reward_points']} points")
        
        print("\n" + "="*60 + "\n")


def main() -> None:
    """Execute the complete mock data generation pipeline.
    
    Orchestrates the full workflow:
    1. Creates 50 Grade 10 students with realistic profiles
    2. Generates 16 curriculum nodes (Math and Science)
    3. Produces 800 mastery records with realistic variation
    4. Exports data to multiple formats (JSON, CSV)
    5. Generates and displays analysis reports
    6. Prints summary statistics and intervention recommendations
    
    This function is the primary entry point for the mock data generator.
    It demonstrates the complete capability of the MockDataGenerator class.
    
    Returns:
        None
    
    Output Files:
        - mock_data.json: Complete dataset in JSON format
        - mock_students.csv: Student records
        - mock_mastery.csv: Mastery assessment records
    
    Example:
        >>> main()  # Generates all mock data and exports files
    """
    print("\n🎮 ThutoQuest-AI Mock Data Generator")
    print("Generating 50 Grade 10 students with varying mastery profiles...\n")
    
    # Create generator
    generator = MockDataGenerator(num_students=50)
    
    # Generate data
    print("📚 Generating students...")
    generator.generate_students()
    
    print("📖 Generating curriculum nodes...")
    generator.generate_curriculum_nodes()
    
    print("📊 Generating mastery scores...")
    generator.generate_mastery_scores()
    
    # Export data
    print("\n💾 Exporting data...")
    generator.export_to_json("mock_data.json")
    generator.export_students_csv("mock_students.csv")
    generator.export_mastery_csv("mock_mastery.csv")
    
    # Print summaries
    generator.print_summary()
    generator.print_critical_gaps_report()
    
    print("✅ Mock data generation complete!")
    print("\nFiles created:")
    print("  - mock_data.json (complete dataset)")
    print("  - mock_students.csv (student records)")
    print("  - mock_mastery.csv (mastery scores)")


if __name__ == "__main__":
    main()
