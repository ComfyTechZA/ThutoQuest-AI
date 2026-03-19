// Utility functions for dashboard

/**
 * Format large numbers with K/M/B suffix
 * @param {number} num - Number to format
 * @returns {string} Formatted string
 */
export const formatNumber = (num) => {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
  if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
  return num.toString();
};

/**
 * Calculate level from points
 * @param {number} points - Total experience points
 * @returns {number} Current level (1-20)
 */
export const calculateLevel = (points) => {
  const pointsPerLevel = 500;
  return Math.min(Math.floor(points / pointsPerLevel) + 1, 20);
};

/**
 * Calculate progress percentage to next level
 * @param {number} points - Current points
 * @returns {number} Progress 0-100
 */
export const calculateLevelProgress = (points) => {
  const pointsPerLevel = 500;
  const currentLevel = Math.floor(points / pointsPerLevel);
  const pointsInCurrentLevel = points - currentLevel * pointsPerLevel;
  return (pointsInCurrentLevel / pointsPerLevel) * 100;
};

/**
 * Get color for difficulty level
 * @param {string} difficulty - Difficulty name
 * @returns {object} Color config
 */
export const getDifficultyConfig = (difficulty) => {
  const config = {
    Beginner: { color: 'emerald', icon: '⭐', value: 1 },
    Intermediate: { color: 'cyan', icon: '⭐⭐', value: 2 },
    Advanced: { color: 'purple', icon: '⭐⭐⭐', value: 3 },
    Expert: { color: 'amber', icon: '⭐⭐⭐⭐', value: 4 },
  };
  return config[difficulty] || config.Beginner;
};

/**
 * Get career icon emoji
 * @param {string} careerTitle - Career name
 * @returns {string} Emoji icon
 */
export const getCareerIcon = (careerTitle) => {
  const icons = {
    'Software Engineer': '💻',
    'Data Scientist': '📊',
    'Physicist': '🔬',
    'Physician': '⚕️',
    'Mathematician': '🧮',
    'Educator': '🎓',
    'Business Analyst': '📈',
    'UX Designer': '🎨',
    'Quality Assurance': '✅',
    'Systems Administrator': '🖥️',
    'Cybersecurity Expert': '🔐',
  };
  return icons[careerTitle] || '🚀';
};

/**
 * Format time remaining
 * @param {number} minutes - Minutes remaining
 * @returns {string} Formatted time
 */
export const formatTimeRemaining = (minutes) => {
  if (minutes < 60) return `${minutes}m left`;
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return `${hours}h ${mins}m left`;
};

/**
 * Check if API is reachable
 * @returns {Promise<boolean>}
 */
export const checkAPIHealth = async () => {
  try {
    const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/health`);
    return response.ok;
  } catch (error) {
    return false;
  }
};

/**
 * Get device performance tier (for conditional rendering)
 * @returns {string} 'low' | 'medium' | 'high'
 */
export const getDevicePerformanceTier = () => {
  if (typeof navigator === 'undefined') return 'high';

  const cores = navigator.hardwareConcurrency || 1;
  const memory = navigator.deviceMemory || 4;

  if (cores <= 2 && memory <= 2) return 'low';
  if (cores <= 4 && memory <= 4) return 'medium';
  return 'high';
};

/**
 * Disable animations for low-end devices
 * @returns {boolean} Should disable animations
 */
export const shouldDisableAnimations = () => {
  const tier = getDevicePerformanceTier();
  return tier === 'low' || window.matchMedia('(prefers-reduced-motion: reduce)').matches;
};

/**
 * Convert mastery score to readable description
 * @param {number} score - Score 0-1
 * @returns {string} Description
 */
export const getMasteryDescription = (score) => {
  if (score >= 0.9) return 'Master';
  if (score >= 0.8) return 'Proficient';
  if (score >= 0.7) return 'Competent';
  if (score >= 0.6) return 'Developing';
  if (score >= 0.5) return 'Emerging';
  return 'Beginner';
};

/**
 * Generate mock student data (for offline development)
 * @param {number} studentNumber - Student ID
 * @returns {object} Mock student data
 */
export const generateMockStudent = (studentNumber = 1) => {
  const firstNames = ['Thabo', 'Nomsa', 'Sipho', 'Lerato', 'Sizwe'];
  const lastNames = ['Mkhize', 'Ndlela', 'Khumalo', 'Nkosi', 'Dlamini'];

  return {
    id: `STU${String(studentNumber).padStart(3, '0')}`,
    name: `${firstNames[studentNumber % firstNames.length]} ${lastNames[studentNumber % lastNames.length]}`,
    grade: 7 + (studentNumber % 6),
    schoolDistrict: ['Gauteng', 'KZN', 'WC', 'Limpopo', 'Eastern Cape'][studentNumber % 5],
    totalPoints: 2000 + studentNumber * 500,
    currentLevel: 3 + (studentNumber % 8),
    streakDays: 5 + (studentNumber % 20),
    masteryScores: {
      mathematics: 0.6 + Math.random() * 0.3,
      science: 0.55 + Math.random() * 0.35,
      coding: 0.5 + Math.random() * 0.4,
      language: 0.7 + Math.random() * 0.25,
      spatial: 0.65 + Math.random() * 0.3,
    },
  };
};
