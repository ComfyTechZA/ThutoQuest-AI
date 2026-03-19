import React, { useState } from 'react';
import QuestMap from '../components/QuestMap';
import CareerRadar from '../components/CareerRadar';
import StatusCard from '../components/StatusCard';
import NavigationBar from '../components/NavigationBar';
import AchievementsBadges from '../components/AchievementsBadges';
import { Zap, TrendingUp, Star } from 'lucide-react';

export default function Dashboard({ studentData }) {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="min-h-screen bg-gradient-to-br from-accent-900 via-primary-900 to-accent-900 text-white pb-24 md:pb-8">
      {/* Header with greeting */}
      <div className="sticky top-0 z-40 bg-gradient-to-b from-accent-900/95 to-accent-900/80 backdrop-blur-lg border-b border-neon-blue/20 px-4 py-4 md:py-6">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h1 className="text-2xl md:text-3xl font-bold bg-gradient-to-r from-neon-blue via-neon-purple to-neon-green bg-clip-text text-transparent">
                Welcome, {studentData.name}
              </h1>
              <p className="text-accent-300 text-sm md:text-base mt-1">Grade {studentData.grade} • {studentData.schoolDistrict}</p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-neon-yellow">{studentData.totalPoints.toLocaleString()}</div>
              <p className="text-accent-400 text-xs md:text-sm">Experience Points</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-6 md:py-8">
        {/* Status Cards Row */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3 md:gap-4 mb-6 md:mb-8">
          <StatusCard
            icon={<Star className="w-5 h-5 md:w-6 md:h-6" />}
            label="Level"
            value={studentData.currentLevel}
            sublabel="Tier"
            color="from-neon-purple to-neon-blue"
          />
          <StatusCard
            icon={<Zap className="w-5 h-5 md:w-6 md:h-6" />}
            label="Streak"
            value={`${studentData.streakDays}d`}
            sublabel="Days Active"
            color="from-neon-yellow to-warning"
          />
          <StatusCard
            icon={<TrendingUp className="w-5 h-5 md:w-6 md:h-6" />}
            label="Progress"
            value={`${studentData.gradeProgress.completed}/${studentData.gradeProgress.nextMilestone}`}
            sublabel="Grades"
            color="from-success to-neon-green"
            className="col-span-2 md:col-span-1"
          />
        </div>

        {/* Tab Navigation */}
        <div className="flex gap-2 mb-6 md:mb-8 border-b border-accent-700/50 overflow-x-auto pb-3">
          {['overview', 'quests', 'skills'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 md:px-6 py-2 font-semibold text-sm md:text-base whitespace-nowrap transition-all ${
                activeTab === tab
                  ? 'text-neon-blue border-b-2 border-neon-blue'
                  : 'text-accent-400 hover:text-accent-200'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        {/* Content Sections */}
        <div className="space-y-6 md:space-y-8">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-6 md:space-y-8 animate-fade-in">
              {/* Quick Stats */}
              <div className="bg-gradient-to-br from-accent-800/40 to-primary-900/40 backdrop-blur-sm border border-neon-blue/30 rounded-2xl p-4 md:p-6">
                <h2 className="text-lg md:text-xl font-bold mb-4 flex items-center gap-2">
                  <span className="w-1 h-6 bg-gradient-to-b from-neon-blue to-neon-purple rounded-full"></span>
                  Your Mastery Profile
                </h2>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-3 md:gap-4">
                  {Object.entries(studentData.masteryScores).map(([skill, score]) => (
                    <div
                      key={skill}
                      className="bg-accent-900/50 rounded-lg p-3 md:p-4 border border-accent-700/50 hover:border-neon-blue/50 transition"
                    >
                      <p className="text-xs md:text-sm text-accent-400 capitalize mb-2">{skill}</p>
                      <div className="w-full bg-accent-700/50 rounded-full h-2 md:h-2.5 overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-neon-blue to-neon-purple rounded-full transition-all duration-500"
                          style={{ width: `${score * 100}%` }}
                        ></div>
                      </div>
                      <p className="text-sm md:text-base font-bold mt-2 text-neon-blue">{(score * 100).toFixed(0)}%</p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Career Predictions */}
              <CareerRadar careersTop3={studentData.careersTop3} masteryScores={studentData.masteryScores} />

              {/* Achievements */}
              <AchievementsBadges totalPoints={studentData.totalPoints} level={studentData.currentLevel} />
            </div>
          )}

          {/* Quests Tab - Quest Map */}
          {activeTab === 'quests' && (
            <QuestMap currentGrade={studentData.gradeProgress.current} totalGrades={13} />
          )}

          {/* Skills Tab */}
          {activeTab === 'skills' && (
            <div className="bg-gradient-to-br from-accent-800/40 to-primary-900/40 backdrop-blur-sm border border-neon-blue/30 rounded-2xl p-4 md:p-6">
              <h2 className="text-lg md:text-xl font-bold mb-4">Skills Development Path</h2>
              <p className="text-accent-300 text-sm md:text-base mb-4">
                Complete quests to unlock new skills and level up in each discipline.
              </p>
              <div className="space-y-3 md:space-y-4">
                {Object.entries(studentData.masteryScores).map(([skill, score]) => (
                  <div key={skill} className="bg-accent-900/50 rounded-lg p-3 md:p-4">
                    <div className="flex justify-between items-center mb-2">
                      <span className="capitalize font-semibold">{skill}</span>
                      <span className="text-neon-blue text-sm md:text-base">{Math.round(score * 100)}%</span>
                    </div>
                    <div className="w-full bg-accent-700 rounded-full h-2 md:h-3 overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-neon-green to-neon-blue rounded-full"
                        style={{ width: `${score * 100}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Navigation Bar */}
      <NavigationBar activeTab={activeTab} onTabChange={setActiveTab} />
    </div>
  );
}
