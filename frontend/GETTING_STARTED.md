# 🚀 Getting Started - ThutoQuest AI Dashboard

## Installation (5 minutes)

### Prerequisites
- Node.js 18+ ([Download](https://nodejs.org))
- npm (comes with Node.js)
- Git (optional)

### 1. Navigate to Frontend
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

Expected output:
```
added 150+ packages in 45s
```

### 3. Start Development Server
```bash
npm run dev
```

Expected output:
```
VITE v5.0.0  ready in 500 ms

➜  Local:   http://localhost:5173/
```

### 4. Open in Browser
**Click**: http://localhost:5173

You should see:
- Hero greeting with student name
- 4 status cards (Level, Streak, Progress, Points)
- Navigation tabs (Overview, Quests, Skills)
- Animated neon dashboard

## 🎮 Try It Out!

### Explore Features
1. **Overview Tab** - See your mastery profile and career radar
2. **Quests Tab** - Browse the 13-grade learning journey
3. **Skills Tab** - Track progress in each STEM area
4. **Mobile Nav** - Tap bottom navigation (on mobile)

### Interact with Components
- Click on grade cards to expand quests
- Hover over achievements to see details
- View radar chart for career analysis
- Read growth recommendations

## 🔧 Configuration

### Edit Mock Data
Edit `src/pages/Dashboard.jsx` (line ~20-40):

```javascript
const mockStudent = {
  name: 'Your Name Here',
  grade: 10,  // Change grade
  totalPoints: 5000,  // Change points
  masteryScores: {
    mathematics: 0.95,  // 0.0 to 1.0
    science: 0.75,
    coding: 0.82,
    language: 0.88,
    spatial: 0.70,
  },
};
```

Save and browser auto-refreshes! ✨

## 📊 Understanding Components

### QuestMap.jsx
Shows 13 years of learning (Grade R to Grade 12):
- Expandable grade cards
- Real DBE curriculum-based quests
- Difficulty ratings and completion tracking
- Horizontal scrollable on mobile

### CareerRadar.jsx
Visualizes STEM skills and career matches:
- Radar chart comparing student vs. benchmark
- Top 3 career recommendations
- Confidence scores
- Recommended skills to develop

### StatusCard.jsx
Gamification metrics:
- Neon glow effects
- Gradient backgrounds
- Hover animations
- Responsive sizing

### AchievementsBadges.jsx
6 collectible achievements:
- Quest Master (10 quests)
- On Fire (7-day streak)
- Rising Star (reach level 5)
- Points Collector (4000+ XP)
- Skill Wizard (unlock all)
- Challenge Champion (5 wins)

## 🎨 Customizing Styling

### Change Theme Colors
Edit `tailwind.config.js`:

```javascript
colors: {
  neon: {
    blue: '#00d9ff',      // Change these
    purple: '#b537f2',
    green: '#00ff88',
    yellow: '#ffb700',
  },
}
```

### Add Custom Classes
In `src/styles/globals.css`:

```css
@layer components {
  .card {
    @apply bg-accent-800/40 border border-neon-blue/30 rounded-2xl p-4;
  }
}
```

Then use: `<div className="card">`

## 🔌 Connect to Backend

When backend is running (from `backend/` folder):

```bash
python src/main.py
```

Update `src/pages/Dashboard.jsx`:

```javascript
// Replace mock data with API call
import { careerService } from '../services/api';

useEffect(() => {
  careerService.predictCareer({
    student_id: 'STU001',
    national_id: '050125TXXXX01',
    age: 15,
    grade: 7,
    school: 'Example',
    district: 'Gauteng'
  }).then(response => {
    setStudentData(response.data);
  });
}, []);
```

## 📱 Mobile Testing

### Browser DevTools
```
1. Press F12 (Dev Tools)
2. Press Ctrl+Shift+M (Device Toolbar)
3. Select device (iPhone 12, Galaxy S21, etc.)
4. Test responsiveness
```

### Real Device
```bash
# On laptop
npm run dev -- --host 0.0.0.0

# On phone (same WiFi):
# Visit http://<laptop-ip>:5173
```

## 🧪 What to Test

- [ ] Dashboard loads in <3 seconds
- [ ] Navigation tabs switch smoothly
- [ ] Quest Map expands/collapses
- [ ] Radar chart displays correctly
- [ ] Achievement badges animate
- [ ] Mobile view is responsive (landscape & portrait)
- [ ] Touch interactions work on phone
- [ ] Dark theme looks good
- [ ] No console errors (F12 > Console)

## 🐛 Troubleshooting

### Issue: Server won't start
```bash
# Error: EADDRINUSE: address already in use :::5173
# Solution: Kill other process
npx kill-port 5173

# Then try again
npm run dev
```

### Issue: Components not updating
```bash
# Solution: Clear cache and restart
rm -rf node_modules/.vite
npm run dev
```

### Issue: Styles not applying
```bash
# Tailwind CSS not compiling
# Solution: Ensure Tailwind is watching
npm run dev

# If still broken:
npm install -D tailwindcss@latest
npm run dev
```

### Issue: Recharts not rendering
```bash
# Check browser console for errors
# Verify ResponsiveContainer has width/height

# In component:
<div style={{ width: '100%', height: 400 }}>
  <ResponsiveContainer width="100%" height="100%">
    <RadarChart data={data}>
      ...
    </RadarChart>
  </ResponsiveContainer>
</div>
```

## 📚 Project Structure Quick Reference

```
frontend/
├── src/
│   └── components/
│       ├── QuestMap.jsx           ← Edit for quest changes
│       ├── CareerRadar.jsx        ← Edit for career display
│       ├── AchievementsBadges.jsx ← Edit for achievements
│       └── StatusCard.jsx         ← Edit for game metrics
│   ├── pages/
│   │   └── Dashboard.jsx          ← Main layout & data
│   ├── services/
│   │   └── api.js                 ← Backend communication
│   ├── utils/
│   │   └── helpers.js             ← Utility functions
│   ├── App.jsx                    ← Root component
│   └── index.jsx                  ← Entry point
├── index.html                     ← Main HTML
├── vite.config.js                 ← Build config
├── tailwind.config.js             ← Theme config
└── package.json                   ← Dependencies
```

## 🎯 Next Steps

1. **Customize Student Data**
   - Edit mock student in Dashboard.jsx
   - Add your own school name/district

2. **Connect Backend**
   - Start backend server
   - Update API_URL in .env
   - Test API calls in browser console

3. **Deploy**
   - Run: `npm run build`
   - Upload `dist/` folder to hosting
   - Set up GitHub Pages / Netlify / Vercel

4. **Mobile App (Optional)**
   - Use React Native
   - Or wrap with Cordova/Capacitor

## 💬 Need Help?

- Check console: Press F12 > Console tab
- Read error messages carefully
- Look in `.md` files for detailed docs
- Review component comments in source code

## 📖 Useful Docs

- [Tailwind CSS](https://tailwindcss.com) - Styling
- [React Docs](https://react.dev) - Framework
- [Vite Docs](https://vitejs.dev) - Build tool
- [Recharts](https://recharts.org) - Charts
- [Lucide Icons](https://lucide.dev) - Icons

---

## ✅ Verification Checklist

After starting `npm run dev`, verify:

- [ ] Browser opens automatically
- [ ] Dashboard loads with student name
- [ ] No errors in console (F12)
- [ ] All 4 hero cards display correctly
- [ ] Tab switching works smoothly
- [ ] Neon colors look good
- [ ] Mobile view responsive (use DevTools)
- [ ] Animations play smoothly
- [ ] Radar chart renders properly
- [ ] Can scroll through grades in Quest Map

If all ✅, you're ready to customize and deploy! 🚀

---

**Starting Dev Server:**
```bash
cd frontend
npm install
npm run dev
```

**Building for Production:**
```bash
npm run build
npm run preview
```

Happy coding! 🎓✨
