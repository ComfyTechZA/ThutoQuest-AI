import React from 'react';
import { Trophy, Flame, Star, Award, Target, Zap } from 'lucide-react';
import clsx from 'clsx';

export default function AchievementsBadges({ totalPoints, level }) {
  const achievements = [
    {
      id: 1,
      title: 'Quest Master',
      description: 'Complete 10 quests',
      icon: Trophy,
      unlocked: true,
      color: 'from-yellow-500 to-yellow-600',
      earned: 'Week 2',
    },
    {
      id: 2,
      title: 'On Fire 🔥',
      description: '7-day streak',
      icon: Flame,
      unlocked: true,
      color: 'from-orange-500 to-red-500',
      earned: 'Day 7',
    },
    {
      id: 3,
      title: 'Rising Star',
      description: 'Reach Level 5',
      icon: Star,
      unlocked: true,
      color: 'from-purple-500 to-pink-500',
      earned: `Level ${level}`,
    },
    {
      id: 4,
      title: 'Points Collector',
      description: '4000+ XP',
      icon: Award,
      unlocked: totalPoints >= 4000,
      color: 'from-emerald-500 to-teal-500',
      earned: totalPoints >= 4000 ? `${totalPoints} XP` : `${totalPoints}/4000 XP`,
    },
    {
      id: 5,
      title: 'Skill Wizard',
      description: 'Unlock all skills',
      icon: Target,
      unlocked: false,
      color: 'from-cyan-500 to-blue-500',
      earned: 'Locked',
    },
    {
      id: 6,
      title: 'Challenge Champion',
      description: 'Win 5 challenges',
      icon: Zap,
      unlocked: false,
      color: 'from-fuchsia-500 to-purple-600',
      earned: 'Locked',
    },
  ];

  return (
    <div className="bg-gradient-to-br from-accent-800/40 to-primary-900/40 backdrop-blur-sm border border-neon-blue/30 rounded-2xl p-4 md:p-6">
      <div className="flex items-center gap-3 mb-4 md:mb-6">
        <Trophy className="w-5 h-5 md:w-6 md:h-6 text-neon-yellow" />
        <h2 className="text-lg md:text-xl font-bold">Achievements & Badges</h2>
      </div>

      {/* Achievements Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3 md:gap-4">
        {achievements.map((achievement) => {
          const Icon = achievement.icon;

          return (
            <div
              key={achievement.id}
              className={clsx(
                'p-3 md:p-4 rounded-xl border-2 transition-all duration-300 hover:scale-105',
                achievement.unlocked
                  ? `bg-gradient-to-br ${achievement.color} bg-opacity-20 border-current border-opacity-50 shadow-lg shadow-current shadow-opacity-20`
                  : 'bg-accent-800/30 border-accent-700/30 opacity-60'
              )}
            >
              <div className="flex flex-col items-center text-center gap-2">
                <div
                  className={clsx(
                    'p-3 rounded-lg transition-all duration-300',
                    achievement.unlocked
                      ? `bg-gradient-to-br ${achievement.color} bg-opacity-30`
                      : 'bg-accent-700/30'
                  )}
                >
                  <Icon
                    className={clsx(
                      'w-6 h-6 md:w-7 md:h-7',
                      achievement.unlocked ? 'text-white' : 'text-accent-500'
                    )}
                  />
                </div>
                <div>
                  <h3 className="font-bold text-sm">{achievement.title}</h3>
                  <p className="text-xs text-accent-400 mt-1">{achievement.description}</p>
                </div>
                <span
                  className={clsx(
                    'text-xs px-2 py-1 rounded-full font-semibold mt-1',
                    achievement.unlocked
                      ? 'bg-success/30 text-success'
                      : 'bg-accent-700/30 text-accent-400'
                  )}
                >
                  {achievement.earned}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Progress to next achievement */}
      <div className="mt-6 md:mt-8 pt-4 md:pt-6 border-t border-accent-700/30">
        <p className="text-sm text-accent-400 mb-3">🎯 Next Achievement: Points Collector (4000+ XP)</p>
        <div className="w-full bg-accent-900/50 rounded-full h-2 md:h-3 overflow-hidden border border-accent-700/30">
          <div
            className="h-full bg-gradient-to-r from-neon-yellow to-warning rounded-full transition-all duration-500"
            style={{ width: `${(totalPoints / 4000) * 100}%` }}
          ></div>
        </div>
        <p className="text-xs md:text-sm text-accent-400 mt-2">
          {4000 - totalPoints} XP to unlock next badge
        </p>
      </div>
    </div>
  );
}
