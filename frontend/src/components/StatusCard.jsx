import React from 'react';
import clsx from 'clsx';

export default function StatusCard({ icon, label, value, sublabel, color = 'from-neon-blue to-neon-purple', className = '' }) {
  return (
    <div className={clsx('relative overflow-hidden rounded-xl md:rounded-2xl p-3 md:p-4 border border-accent-700/50 hover:border-accent-600 transition-all duration-300 group', className)}>
      {/* Gradient Background */}
      <div className={clsx(`absolute inset-0 bg-gradient-to-br ${color} opacity-10 group-hover:opacity-20 transition-opacity`, 'rounded-xl md:rounded-2xl')}></div>

      {/* Neon Glow Effect */}
      <div className={`absolute -inset-1 bg-gradient-to-b ${color} opacity-0 group-hover:opacity-20 blur-xl transition-opacity duration-300 -z-10 rounded-xl md:rounded-2xl`}></div>

      {/* Content */}
      <div className="relative z-10">
        <div className="flex justify-between items-start gap-2 mb-2">
          <div className={`p-2 md:p-2.5 rounded-lg bg-gradient-to-br ${color} bg-opacity-20 border border-current border-opacity-30`}>
            <div className="text-accent-300">{icon}</div>
          </div>
          <p className="text-xs md:text-sm text-accent-400 font-medium">{label}</p>
        </div>
        <div className="mt-3">
          <p className="text-2xl md:text-3xl font-bold bg-gradient-to-r from-neon-blue via-neon-purple to-neon-green bg-clip-text text-transparent">
            {value}
          </p>
          <p className="text-xs md:text-sm text-accent-400 mt-1">{sublabel}</p>
        </div>
      </div>

      {/* Animated Border */}
      <div className="absolute inset-0 rounded-xl md:rounded-2xl bg-gradient-to-r from-neon-blue via-neon-purple to-neon-green bg-size-200 opacity-0 group-hover:opacity-10 transition-opacity duration-300 pointer-events-none"></div>
    </div>
  );
}
