import React, { useState, useEffect } from 'react';
import Dashboard from './pages/Dashboard';
import './styles/globals.css';

export default function App() {
  const [studentData, setStudentData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Mock student data - replace with actual API call
    const mockStudent = {
      id: 'STU001',
      name: 'Thabo Mkhize',
      grade: 7,
      schoolDistrict: 'Gauteng',
      totalPoints: 4250,
      currentLevel: 5,
      streakDays: 12,
      masteryScores: {
        mathematics: 0.82,
        science: 0.75,
        coding: 0.68,
        language: 0.79,
        spatial: 0.71,
      },
      careersTop3: [
        { title: 'Software Engineer', confidence: 0.89, icon: '💻' },
        { title: 'Data Scientist', confidence: 0.85, icon: '📊' },
        { title: 'Physicist', confidence: 0.78, icon: '🔬' },
      ],
      gradeProgress: {
        current: 7,
        completed: 6,
        nextMilestone: 8,
      },
    };

    // Simulate API delay
    setTimeout(() => {
      setStudentData(mockStudent);
      setLoading(false);
    }, 800);
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-accent-900 via-primary-900 to-accent-900 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block">
            <div className="w-16 h-16 border-4 border-neon-blue border-t-neon-purple rounded-full animate-spin"></div>
          </div>
          <p className="mt-4 text-white text-lg font-semibold">Loading your quest...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-accent-900 via-primary-900 to-accent-900 flex items-center justify-center p-4">
        <div className="text-center">
          <p className="text-danger text-lg">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="mt-4 px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-accent-900 via-primary-900 to-accent-900">
      {studentData && <Dashboard studentData={studentData} />}
    </div>
  );
}
