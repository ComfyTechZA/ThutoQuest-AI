# ThutoQuest AI Frontend - Development Setup

## Quick Start Guide (5 minutes)

### Step 1: Navigate to Frontend
```bash
cd frontend
```

### Step 2: Install Dependencies
```bash
npm install
```

This installs:
- React 18.2
- Vite 5.0 (ultra-fast build tool)
- Tailwind CSS (styling)
- Recharts (data visualization)
- Lucide React (icons)

### Step 3: Start Development Server
```bash
npm run dev
```

Open browser: **http://localhost:5173**

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── QuestMap.jsx        ← 13-grade journey map
│   │   ├── CareerRadar.jsx     ← STEM skills visualization
│   │   ├── StatusCard.jsx      ← Gamification metrics
│   │   ├── NavigationBar.jsx   ← Mobile bottom nav
│   │   └── AchievementsBadges.jsx ← Badges display
│   ├── pages/
│   │   └── Dashboard.jsx       ← Main layout
│   ├── services/
│   │   └── api.js              ← Backend API calls
│   ├── hooks/
│   │   └── useCustomHooks.js   ← Custom React hooks
│   ├── styles/
│   │   └── globals.css         ← Global styling
│   ├── App.jsx                 ← Root component
│   └── index.jsx               ← Entry point
├── index.html                  ← HTML template
├── vite.config.js              ← Build config
├── tailwind.config.js          ← Theme config
└── package.json                ← Dependencies
```

## 🎯 Key Features Implemented

### 1. Quest Map
- Shows all 13 grades (R → 12)
- Real DBE curriculum-based quests
- Status indicators: ✓ Completed | ⚡ In Progress | 🔒 Locked
- Difficulty levels with star ratings
- Horizontal scroll on mobile, grid on desktop

### 2. AI Career Radar
- Radar chart visualizing 5 STEM skills
- Top 3 career matches with confidence scores
- Growth recommendations
- Skill-based career suggestions

### 3. Gamification
- Points, levels, streaks
- 6 achievement badges
- Progress bars for each skill
- Status cards with neon glow effects

### 4. Mobile Optimization
- Responsive 320px → 1200px+
- Touch-optimized (44px min buttons)
- Notch/safe-area support for modern phones
- 3G-friendly (280KB gzipped)
- Low-end device optimized (1GB RAM tested)

## 🎨 Design System

### Colors
```css
Primary: Cyan (#0ea5e9)
Accent: Dark Navy (#0f172a)
Neon Blue: #00d9ff
Neon Purple: #b537f2
Neon Green: #00ff88
Neon Yellow: #ffb700
Success: #10b981
```

### Typography
```css
Body: Inter (14-16px on mobile, 16-18px on desktop)
Font Weight: 400 (regular), 600 (semibold), 700 (bold), 800 (extrabold)
```

## 🚀 Development Workflow

### 1. Add New Component
```bash
# Create in src/components/MyComponent.jsx
import React from 'react';
import clsx from 'clsx';

export default function MyComponent() {
  return (
    <div className="bg-accent-800/40 rounded-xl p-4 border border-neon-blue/30">
      {/* Your content */}
    </div>
  );
}
```

### 2. Use Tailwind Classes
```jsx
// Responsive
<div className="text-sm md:text-base lg:text-lg">

// Colors
<div className="bg-neon-blue text-neon-purple">

// Effects
<div className="hover:scale-105 transition-all duration-300">
<div className="animate-pulse shadow-lg shadow-neon-blue/30">
```

### 3. Import Icons
```jsx
import { Star, Zap, Trophy, Award } from 'lucide-react';

<Star className="w-5 h-5 text-neon-yellow" />
```

## 📊 Testing Components Locally

Edit `src/App.jsx` mock data to test different scenarios:

```javascript
const mockStudent = {
  name: 'Test Student',
  grade: 7,
  totalPoints: 2500,  // Change to test thresholds
  masteryScores: {
    mathematics: 0.5,  // Change to test radar chart
    science: 0.8,
    // ...
  },
};
```

## 🔌 Backend Integration

The API service is in `src/services/api.js`:

```javascript
// Call career prediction endpoint
import { careerService } from './services/api';

const response = await careerService.predictCareer({
  student_id: 'STU001',
  national_id: '050125TXXXX01',
  age: 15,
  grade: 7,
  school: 'Example',
  district: 'Gauteng'
});
```

Currently uses **mock data**. To enable real API:
1. Start backend: `python src/main.py` (from backend/)
2. Update `.env`: `VITE_API_URL=http://localhost:8000/api/v1`
3. Replace mock data in `Dashboard.jsx` with API calls

## 🛠️ Build & Deploy

### Development Build
```bash
npm run dev
```

### Production Build
```bash
npm run build
```

Output: `dist/` folder (ready for hosting)

### Preview Production Build Locally
```bash
npm run preview
```

## ⚡ Performance Tips

1. **Use Lazy Loading**
   ```jsx
   import { Suspense, lazy } from 'react';
   const CareerRadar = lazy(() => import('./CareerRadar'));
   
   <Suspense fallback={<div>Loading...</div>}>
     <CareerRadar />
   </Suspense>
   ```

2. **Memoize Components**
   ```jsx
   const StatusCard = React.memo(function StatusCard(props) {
     // Component code
   });
   ```

3. **Use Tailwind CSS Properly**
   - Avoid inline styles
   - Use utility classes
   - Let PurgeCSS remove unused styles in production

## 🐛 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| Slow on 3G | Enable offline mode in `.env` |
| Buttons not clickable | Check min-height (44px) is preserved |
| Neon glow too bright | Reduce `opacity-20` to `opacity-10` |
| Notch overlaps content | CSS handles `env(safe-area-inset-*)` auto |
| Chart not rendering | Check recharts is imported correctly |

## 📚 Resources

- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [React Docs](https://react.dev)
- [Vite Docs](https://vitejs.dev)
- [Recharts Docs](https://recharts.org)
- [Lucide Icons](https://lucide.dev)

## 🤝 Contributing

1. Create features in new branches
2. Test on mobile (use DevTools device emulation)
3. Ensure responsive on 320px and 1200px+
4. Keep bundle size under 300KB (gzipped)

## 📝 Deployment Checklist

- [ ] Build passes without errors: `npm run build`
- [ ] No console errors in production build
- [ ] Tested on low-end Android device
- [ ] API endpoints configured in `.env`
- [ ] Meta tags updated for mobile
- [ ] Performance: Lighthouse 90+ score

---

**Happy Coding! 🚀**

Start dev server: `npm run dev`  
View docs: `http://localhost:5173`
