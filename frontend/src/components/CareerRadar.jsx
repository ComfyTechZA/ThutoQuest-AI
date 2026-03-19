import React, { useMemo } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { Briefcase, TrendingUp, Zap } from 'lucide-react';
import clsx from 'clsx';

export default function CareerRadar({ careersTop3, masteryScores }) {
  // Transform mastery scores for radar chart
  const radarData = useMemo(() => {
    return Object.entries(masteryScores).map(([skill, score]) => ({
      subject: skill.charAt(0).toUpperCase() + skill.slice(1),
      'Your Score': Math.round(score * 100),
      'Benchmark': 75, // Average benchmark
      fullMark: 100,
    }));
  }, [masteryScores]);

  const getCareerIcon = (title) => {
    const icons = {
      'Software Engineer': '💻',
      'Data Scientist': '📊',
      'Physicist': '🔬',
      'Physician': '⚕️',
      'Mathematician': '🧮',
      'Educator': '🎓',
    };
    return icons[title] || '🚀';
  };

  return (
    <div className="space-y-6 md:space-y-8">
      {/* Main Career Radar Chart */}
      <div className="bg-gradient-to-br from-accent-800/40 to-primary-900/40 backdrop-blur-sm border border-neon-blue/30 rounded-2xl p-4 md:p-6 overflow-hidden">
        <div className="flex items-center gap-3 mb-4 md:mb-6">
          <div className="w-1 h-8 bg-gradient-to-b from-neon-purple to-neon-blue rounded-full"></div>
          <h2 className="text-lg md:text-xl font-bold">AI Career Radar</h2>
        </div>

        {/* Radar Chart - Responsive */}
        <div className="w-full h-80 md:h-96 -mx-4 md:mx-0">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={radarData} margin={{ top: 20, right: 30, bottom: 20, left: 30 }}>
              <PolarGrid stroke="#334155" strokeDasharray="3 3" />
              <PolarAngleAxis 
                dataKey="subject" 
                tick={{ fill: '#cbd5e1', fontSize: 12 }}
                angle={90}
                direction="clockwise"
              />
              <PolarRadiusAxis 
                angle={90} 
                domain={[0, 100]} 
                tick={{ fill: '#94a3b8', fontSize: 10 }}
              />
              <Radar 
                name="Your Score" 
                dataKey="Your Score" 
                stroke="#00d9ff" 
                fill="#00d9ff" 
                fillOpacity={0.2}
                strokeWidth={2}
              />
              <Radar 
                name="Benchmark" 
                dataKey="Benchmark" 
                stroke="#b537f2" 
                fill="#b537f2" 
                fillOpacity={0.1}
                strokeWidth={1}
                strokeDasharray="5 5"
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#0f172a',
                  border: '1px solid #00d9ff',
                  borderRadius: '8px',
                  color: '#0f172a',
                }}
                labelStyle={{ color: '#0f172a' }}
              />
              <Legend 
                wrapperStyle={{ paddingTop: '20px' }}
                iconType="circle"
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        <p className="text-xs md:text-sm text-accent-400 mt-4 text-center">
          💡 Your skills compared to industry standards. Higher coverage = better career match.
        </p>
      </div>

      {/* Top Career Recommendations */}
      <div className="bg-gradient-to-br from-accent-800/40 to-primary-900/40 backdrop-blur-sm border border-neon-blue/30 rounded-2xl p-4 md:p-6">
        <div className="flex items-center gap-3 mb-4 md:mb-6">
          <Briefcase className="w-5 h-5 md:w-6 md:h-6 text-neon-yellow" />
          <h2 className="text-lg md:text-xl font-bold">Top Career Matches</h2>
        </div>

        <div className="space-y-3 md:space-y-4">
          {careersTop3.map((career, index) => (
            <div
              key={index}
              className={clsx(
                'p-4 md:p-5 rounded-xl border transition-all duration-300 hover:scale-105 hover:shadow-lg',
                index === 0
                  ? 'bg-gradient-to-r from-neon-yellow/20 to-warning/10 border-neon-yellow/50 ring-1 ring-neon-yellow/30'
                  : index === 1
                    ? 'bg-gradient-to-r from-neon-blue/20 to-primary-500/10 border-neon-blue/50'
                    : 'bg-gradient-to-r from-neon-purple/20 to-primary-700/10 border-neon-purple/50'
              )}
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  <span className="text-2xl md:text-3xl">{getCareerIcon(career.title)}</span>
                  <div className="min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className="text-sm md:text-base font-bold">{career.title}</h3>
                      {index === 0 && (
                        <span className="bg-neon-yellow/40 text-neon-yellow text-xs px-2 py-0.5 rounded-full font-semibold">
                          🎯 Best Match
                        </span>
                      )}
                    </div>
                    <p className="text-xs md:text-sm text-accent-400 mt-1">STEM Career Path</p>
                  </div>
                </div>
              </div>

              {/* Confidence Meter */}
              <div className="mb-3">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-xs md:text-sm text-accent-400">Career Match</span>
                  <span
                    className={clsx(
                      'text-sm md:text-base font-bold',
                      career.confidence >= 0.85 ? 'text-success' : career.confidence >= 0.75 ? 'text-neon-blue' : 'text-warning'
                    )}
                  >
                    {Math.round(career.confidence * 100)}%
                  </span>
                </div>
                <div className="w-full bg-accent-900/50 rounded-full h-2 md:h-2.5 overflow-hidden border border-accent-700/30">
                  <div
                    className={clsx(
                      'h-full rounded-full transition-all duration-500',
                      career.confidence >= 0.85
                        ? 'bg-gradient-to-r from-success to-neon-green'
                        : career.confidence >= 0.75
                          ? 'bg-gradient-to-r from-neon-blue to-neon-purple'
                          : 'bg-gradient-to-r from-warning to-neon-yellow'
                    )}
                    style={{ width: `${career.confidence * 100}%` }}
                  ></div>
                </div>
              </div>

              {/* Recommended Skills */}
              <div className="bg-accent-900/30 rounded-lg p-2 md:p-3">
                <p className="text-xs text-accent-400 mb-2">Skills to develop:</p>
                <div className="flex flex-wrap gap-1 md:gap-2">
                  {career.title === 'Software Engineer' && (
                    <>
                      <span className="text-xs px-2 py-1 bg-neon-blue/20 text-neon-blue rounded border border-neon-blue/40">
                        Coding
                      </span>
                      <span className="text-xs px-2 py-1 bg-neon-blue/20 text-neon-blue rounded border border-neon-blue/40">
                        Algorithms
                      </span>
                      <span className="text-xs px-2 py-1 bg-neon-blue/20 text-neon-blue rounded border border-neon-blue/40">
                        Problem Solving
                      </span>
                    </>
                  )}
                  {career.title === 'Data Scientist' && (
                    <>
                      <span className="text-xs px-2 py-1 bg-neon-purple/20 text-neon-purple rounded border border-neon-purple/40">
                        Statistics
                      </span>
                      <span className="text-xs px-2 py-1 bg-neon-purple/20 text-neon-purple rounded border border-neon-purple/40">
                        Python
                      </span>
                      <span className="text-xs px-2 py-1 bg-neon-purple/20 text-neon-purple rounded border border-neon-purple/40">
                        Data Visualization
                      </span>
                    </>
                  )}
                  {career.title === 'Physicist' && (
                    <>
                      <span className="text-xs px-2 py-1 bg-neon-green/20 text-neon-green rounded border border-neon-green/40">
                        Physics
                      </span>
                      <span className="text-xs px-2 py-1 bg-neon-green/20 text-neon-green rounded border border-neon-green/40">
                        Mathematics
                      </span>
                      <span className="text-xs px-2 py-1 bg-neon-green/20 text-neon-green rounded border border-neon-green/40">
                        Experimentation
                      </span>
                    </>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Career Growth Tips */}
      <div className="bg-gradient-to-br from-accent-800/40 to-primary-900/40 backdrop-blur-sm border border-neon-blue/30 rounded-2xl p-4 md:p-6">
        <div className="flex items-center gap-3 mb-4">
          <TrendingUp className="w-5 h-5 md:w-6 md:h-6 text-neon-green" />
          <h3 className="text-base md:text-lg font-bold">Growth Recommendations</h3>
        </div>
        <ul className="space-y-2 text-sm md:text-base text-accent-300">
          <li className="flex gap-2">
            <span className="text-neon-yellow flex-shrink-0">→</span>
            <span>Focus on coding challenges to boost Software Engineer match (+15%)</span>
          </li>
          <li className="flex gap-2">
            <span className="text-neon-yellow flex-shrink-0">→</span>
            <span>Complete data analysis quests to strengthen Data Scientist path</span>
          </li>
          <li className="flex gap-2">
            <span className="text-neon-yellow flex-shrink-0">→</span>
            <span>Improve consistency in science topics (currently 75%, aim for 85%)</span>
          </li>
        </ul>
      </div>
    </div>
  );
}
