import React from 'react';
import { Home, Map, Zap, User, Settings } from 'lucide-react';
import clsx from 'clsx';

export default function NavigationBar({ activeTab, onTabChange }) {
  const navItems = [
    { id: 'overview', label: 'Overview', icon: Home },
    { id: 'quests', label: 'Quests', icon: Map },
    { id: 'skills', label: 'Skills', icon: Zap },
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div className="fixed bottom-0 left-0 right-0 md:hidden">
      {/* Mobile Navigation Bar */}
      <div className="bg-gradient-to-t from-accent-900/95 to-accent-900/80 backdrop-blur-lg border-t border-neon-blue/20 px-2 py-3 flex justify-around safe-bottom">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;

          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              className={clsx(
                'flex flex-col items-center justify-center py-2 px-3 rounded-lg transition-all duration-300 text-xs font-medium',
                isActive
                  ? 'bg-gradient-to-b from-neon-blue/30 to-neon-purple/20 text-neon-blue shadow-lg shadow-neon-blue/20'
                  : 'text-accent-400 hover:text-accent-200 hover:bg-accent-800/30'
              )}
            >
              <Icon className={clsx('w-5 h-5 mb-1', isActive && 'animate-pulse')} />
              <span className="truncate">{item.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
