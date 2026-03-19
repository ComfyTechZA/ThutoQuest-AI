import React, { useState } from 'react';
import { ChevronRight, Lock, CheckCircle, Zap, Award } from 'lucide-react';
import clsx from 'clsx';

export default function QuestMap({ currentGrade = 7, totalGrades = 13 }) {
  const [expandedGrade, setExpandedGrade] = useState(currentGrade);

  // Define quests for each grade using real South African curriculum
  const grades = [
    {
      number: 'R',
      name: 'Reception',
      quests: [
        { id: 1, title: 'Number Friends (0-5)', difficulty: 'Beginner', completed: true },
        { id: 2, title: 'Shape Explorer', difficulty: 'Beginner', completed: true },
      ],
    },
    {
      number: 1,
      name: 'Grade 1',
      quests: [
        { id: 3, title: 'Counting to 20', difficulty: 'Beginner', completed: true },
        { id: 4, title: 'Basic Addition', difficulty: 'Beginner', completed: true },
      ],
    },
    {
      number: 2,
      name: 'Grade 2',
      quests: [
        { id: 5, title: 'Two-Digit Numbers', difficulty: 'Beginner', completed: true },
        { id: 6, title: 'Subtraction Quest', difficulty: 'Intermediate', completed: true },
      ],
    },
    {
      number: 3,
      name: 'Grade 3',
      quests: [
        { id: 7, title: 'Multiplication Basics', difficulty: 'Intermediate', completed: true },
        { id: 8, title: 'Fractions (1/2, 1/4)', difficulty: 'Intermediate', completed: true },
      ],
    },
    {
      number: 4,
      name: 'Grade 4',
      quests: [
        { id: 9, title: 'Long Division', difficulty: 'Intermediate', completed: true },
        { id: 10, title: 'Decimals Intro', difficulty: 'Intermediate', completed: true },
      ],
    },
    {
      number: 5,
      name: 'Grade 5',
      quests: [
        { id: 11, title: 'Percentage Calculator', difficulty: 'Intermediate', completed: true },
        { id: 12, title: 'Data Handling', difficulty: 'Advanced', completed: true },
      ],
    },
    {
      number: 6,
      name: 'Grade 6',
      quests: [
        { id: 13, title: 'Algebra Fundamentals', difficulty: 'Advanced', completed: true },
        { id: 14, title: 'Geometry Patterns', difficulty: 'Advanced', completed: true },
      ],
    },
    {
      number: 7,
      name: 'Grade 7 - YOU ARE HERE',
      quests: [
        { id: 15, title: 'Equations & Variables', difficulty: 'Advanced', completed: false, inProgress: true },
        { id: 16, title: 'Data Analysis', difficulty: 'Advanced', completed: false, inProgress: false },
        { id: 17, title: 'Coding: Loops', difficulty: 'Advanced', completed: false, inProgress: false },
      ],
    },
    {
      number: 8,
      name: 'Grade 8',
      quests: [
        { id: 18, title: 'Advanced Algebra', difficulty: 'Expert', completed: false },
        { id: 19, title: 'Statistics', difficulty: 'Expert', completed: false },
      ],
    },
    {
      number: 9,
      name: 'Grade 9',
      quests: [
        { id: 20, title: 'Functions & Graphs', difficulty: 'Expert', completed: false },
        { id: 21, title: 'Coding: OOP', difficulty: 'Expert', completed: false },
      ],
    },
    {
      number: 10,
      name: 'Grade 10',
      quests: [
        { id: 22, title: 'Trigonometry', difficulty: 'Expert', completed: false },
        { id: 23, title: 'Physics Basics', difficulty: 'Expert', completed: false },
      ],
    },
    {
      number: 11,
      name: 'Grade 11',
      quests: [
        { id: 24, title: 'Calculus Intro', difficulty: 'Expert', completed: false },
        { id: 25, title: 'Chemistry Reactions', difficulty: 'Expert', completed: false },
      ],
    },
    {
      number: 12,
      name: 'Grade 12 - Matric',
      quests: [
        { id: 26, title: 'Advanced Calculus', difficulty: 'Expert', completed: false },
        { id: 27, title: 'Final Project', difficulty: 'Expert', completed: false },
      ],
    },
  ];

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'Beginner':
        return 'text-emerald-400 bg-emerald-900/30';
      case 'Intermediate':
        return 'text-cyan-400 bg-cyan-900/30';
      case 'Advanced':
        return 'text-purple-400 bg-purple-900/30';
      case 'Expert':
        return 'text-amber-400 bg-amber-900/30';
      default:
        return 'text-accent-400';
    }
  };

  const getDifficultyIcon = (difficulty) => {
    switch (difficulty) {
      case 'Beginner':
        return '⭐';
      case 'Intermediate':
        return '⭐⭐';
      case 'Advanced':
        return '⭐⭐⭐';
      case 'Expert':
        return '⭐⭐⭐⭐';
      default:
        return '';
    }
  };

  return (
    <div className="space-y-4 md:space-y-6">
      <div className="bg-gradient-to-br from-accent-800/40 to-primary-900/40 backdrop-blur-sm border border-neon-blue/30 rounded-2xl p-4 md:p-6">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-1 h-8 bg-gradient-to-b from-neon-blue to-neon-purple rounded-full"></div>
          <div>
            <h2 className="text-lg md:text-2xl font-bold">Your Quest Map</h2>
            <p className="text-accent-300 text-xs md:text-sm">13-Year Learning Journey • Grade R to Grade 12</p>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mb-6 md:mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-xs md:text-sm text-accent-400">Overall Progress</span>
            <span className="text-sm md:text-base font-bold text-neon-green">{Math.round((currentGrade / totalGrades) * 100)}%</span>
          </div>
          <div className="w-full bg-accent-900/50 rounded-full h-3 md:h-4 overflow-hidden border border-accent-700/30">
            <div
              className="h-full bg-gradient-to-r from-neon-green via-neon-blue to-neon-purple rounded-full transition-all duration-700"
              style={{ width: `${(currentGrade / totalGrades) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Grades Timeline - Scrollable on mobile */}
        <div className="overflow-x-auto md:overflow-x-visible pb-4 md:pb-0">
          <div className="flex md:grid md:grid-cols-1 gap-3 md:gap-4 min-w-max md:min-w-0">
            {grades.map((grade, index) => {
              const isCompleted = parseInt(grade.number) !== 'R' && parseInt(grade.number) < currentGrade;
              const isCurrent = parseInt(grade.number) === currentGrade;
              const isLocked = parseInt(grade.number) > currentGrade;

              return (
                <div key={index} className="w-64 md:w-full flex-shrink-0 md:flex-shrink">
                  <button
                    onClick={() => setExpandedGrade(grade.number)}
                    className={clsx(
                      'w-full p-3 md:p-4 rounded-xl border-2 transition-all duration-300',
                      isCurrent
                        ? 'bg-primary-900/60 border-neon-blue/80 shadow-lg shadow-neon-blue/30'
                        : isCompleted
                          ? 'bg-accent-800/50 border-success/50 hover:border-success'
                          : isLocked
                            ? 'bg-accent-900/30 border-accent-700/30 opacity-60'
                            : 'bg-accent-800/40 border-accent-700/50 hover:border-neon-purple/50'
                    )}
                  >
                    <div className="flex items-center justify-between">
                      <div className="text-left">
                        <div className="flex items-center gap-2">
                          {isCompleted && <CheckCircle className="w-4 h-4 md:w-5 md:h-5 text-success" />}
                          {isCurrent && <Zap className="w-4 h-4 md:w-5 md:h-5 text-neon-yellow animate-pulse" />}
                          {isLocked && <Lock className="w-4 h-4 md:w-5 md:h-5 text-accent-500" />}
                          <span className="font-bold text-sm md:text-base">{grade.number}</span>
                        </div>
                        <p className="text-xs md:text-sm text-accent-400 mt-1">{grade.name}</p>
                      </div>
                      {expandedGrade === grade.number && (
                        <ChevronRight className="w-5 h-5 md:w-6 md:h-6 text-neon-blue transform rotate-90" />
                      )}
                    </div>
                  </button>

                  {/* Expanded Quest List */}
                  {expandedGrade === grade.number && (
                    <div className="mt-3 md:mt-4 space-y-2 md:space-y-3 animate-fade-in">
                      {grade.quests.map((quest) => (
                        <div
                          key={quest.id}
                          className={clsx(
                            'p-3 md:p-4 rounded-lg border transition-all duration-300',
                            quest.completed
                              ? 'bg-success/10 border-success/40'
                              : quest.inProgress
                                ? 'bg-neon-yellow/10 border-neon-yellow/40 ring-1 ring-neon-yellow/30'
                                : 'bg-accent-800/30 border-accent-700/40'
                          )}
                        >
                          <div className="flex items-start justify-between gap-2 md:gap-3">
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 mb-2">
                                {quest.completed && <CheckCircle className="w-4 h-4 md:w-5 md:h-5 text-success flex-shrink-0" />}
                                {quest.inProgress && <Zap className="w-4 h-4 md:w-5 md:h-5 text-neon-yellow flex-shrink-0 animate-bounce" />}
                                <h4 className="font-semibold text-sm md:text-base truncate">{quest.title}</h4>
                              </div>
                              <span className={clsx('text-xs md:text-sm px-2 py-1 rounded-full inline-block', getDifficultyColor(quest.difficulty))}>
                                {getDifficultyIcon(quest.difficulty)} {quest.difficulty}
                              </span>
                            </div>
                            {quest.completed && <Award className="w-4 h-4 md:w-5 md:h-5 text-success flex-shrink-0" />}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Legend */}
        <div className="mt-6 md:mt-8 pt-4 md:pt-6 border-t border-accent-700/30">
          <p className="text-xs md:text-sm text-accent-400 mb-3">Progress Legend:</p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-2 md:gap-3 text-xs md:text-sm">
            <div className="flex items-center gap-2">
              <CheckCircle className="w-4 h-4 text-success" />
              <span className="text-accent-300">Completed</span>
            </div>
            <div className="flex items-center gap-2">
              <Zap className="w-4 h-4 text-neon-yellow" />
              <span className="text-accent-300">In Progress</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-4 h-4 bg-accent-600 rounded"></div>
              <span className="text-accent-300">Available</span>
            </div>
            <div className="flex items-center gap-2">
              <Lock className="w-4 h-4 text-accent-500" />
              <span className="text-accent-300">Locked</span>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="grid grid-cols-2 gap-3 md:gap-4">
        <div className="bg-gradient-to-br from-success/20 to-primary-900/40 border border-success/30 rounded-xl p-3 md:p-4">
          <p className="text-accent-400 text-xs md:text-sm mb-1">Grades Completed</p>
          <p className="text-2xl md:text-3xl font-bold text-success">{currentGrade}</p>
        </div>
        <div className="bg-gradient-to-br from-neon-blue/20 to-primary-900/40 border border-neon-blue/30 rounded-xl p-3 md:p-4">
          <p className="text-accent-400 text-xs md:text-sm mb-1">Quests Remaining</p>
          <p className="text-2xl md:text-3xl font-bold text-neon-blue">{grades.length - currentGrade}</p>
        </div>
      </div>
    </div>
  );
}
