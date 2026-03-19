# ThutoQuest-AI Technical Specifications

## Document Control
- **Version**: 1.0
- **Date**: March 2026
- **Author**: AI Development Team
- **Status**: ACTIVE

---

## 1. System Architecture Overview

### Layered Architecture
```
┌─────────────────────────────────────┐
│     Interfaces Layer                 │ API Routes, Controllers
├─────────────────────────────────────┤
│     Application Layer                │ Use Cases, Services
├─────────────────────────────────────┤
│     Domain Layer                     │ Business Logic, Models
├─────────────────────────────────────┤
│     Infrastructure Layer             │ Database, External APIs
└─────────────────────────────────────┘
```

### Technology Stack
| Layer | Technology | Rationale |
|-------|-----------|-----------|
| API Server | FastAPI | Async-capable, auto-docs, high performance |
| Database | PostgreSQL | ACID compliance, JSON support, Ext. ecosystem |
| ORM | SQLAlchemy | Type-safe, database-agnostic |
| ML/Analytics | Python (scikit-learn, pandas) | Rich ecosystem for education analytics |
| Frontend | React/Vue | Real-time dashboards, interactive components |
| Mobile | React Native | Code sharing, native performance |
| Auth | JWT + OAuth2 | Standard, stateless, scalable |
| Cache | Redis | Low-latency, session management |

---

## 2. Data Model Specifications

### 2.1 Core Entities

#### STUDENT
```sql
id: UUID (PK)
national_id: VARCHAR(20) UNIQUE
first_name, last_name: VARCHAR
email: VARCHAR UNIQUE
grade_level: INT (8-12)
school_id: FK → schools
learning_style: ENUM('visual', 'auditory', 'kinesthetic', 'mixed')
avatar_id: FK → cosmetics
created_at, updated_at: TIMESTAMP
is_active: BOOLEAN
```

**Relationships**:
- 1 Student : N Mastery Records
- 1 Student : N Assessment Results
- 1 Student : 1 Learning Profile
- 1 Student : N Group Memberships
- 1 Student : N Achievements

#### CURRICULUM_NODE
```sql
id: UUID (PK)
subject: ENUM('Mathematics', 'Science', ...)
topic_name: VARCHAR
grade_level: INT (8-12)
description: TEXT
learning_outcomes: TEXT
bloom_level: ENUM('remember', 'understand', 'apply', 'analyze', 'evaluate', 'create')
difficulty_level: ENUM('Easy', 'Medium', 'Hard')
estimated_hours: INT
prerequisite_nodes: FK[] → curriculum_nodes (self-reference)
parent_unit_id: FK → curriculum_nodes (for hierarchies)
```

#### MASTERY_GRAPH
```sql
id: UUID (PK)
student_id: FK → students
curriculum_node_id: FK → curriculum_nodes
mastery_score: DECIMAL(3,2) [0.0, 1.0]
confidence_interval: DECIMAL → Learning analytics
last_assessment_date: TIMESTAMP
number_of_attempts: INT
time_spent_minutes: INT
is_mastered: BOOLEAN (generated: mastery_score >= 0.8)
status: ENUM('Not Started', 'In Progress', 'Completed', 'Mastered')
retention_score: DECIMAL → Spaced repetition metric
next_review_date: TIMESTAMP → Spaced repetition schedule
```

#### ASSESSMENT_RESULT
```sql
id: UUID (PK)
mastery_graph_id: FK → mastery_graph
student_id: FK → students
curriculum_node_id: FK → curriculum_nodes
score: DECIMAL(3,2)
questions_correct, questions_total: INT
assessment_type: ENUM('Quiz', 'Test', 'Assignment', 'Project', 'Adaptive')
item_ids: UUID[] → assessment_items (which questions)
time_spent_seconds: INT
difficulty_presented: ENUM('Easy', 'Medium', 'Hard')
adaptive_level_adjusted: BOOLEAN
attempted_at: TIMESTAMP
item_response_theory_theta: DECIMAL → IRT ability estimate
```

#### NEW: ACHIEVEMENT
```sql
id: UUID (PK)
achievement_key: VARCHAR UNIQUE ('math_wizard', 'perseverance_hero', etc.)
name, description: VARCHAR
icon_url: VARCHAR
rarity: ENUM('Common', 'Rare', 'Epic', 'Legendary')
unlock_condition: JSONB (trigger definition)
points_reward: INT
created_at: TIMESTAMP
```

#### NEW: STUDENT_ACHIEVEMENT
```sql
id: UUID (PK)
student_id: FK → students
achievement_id: FK → achievements
unlocked_at: TIMESTAMP
```

#### NEW: LEADERBOARD_ENTRY
```sql
id: UUID (PK)
student_id: FK → students
leaderboard_type: ENUM('subject', 'school', 'national', 'skill')
period: ENUM('daily', 'weekly', 'monthly', 'all_time')
rank: INT
score: INT (computed from weighted metrics)
updated_at: TIMESTAMP
```

#### NEW: ASSESSMENT_ITEM
```sql
id: UUID (PK)
question_text: TEXT
question_type: ENUM('mcq', 'short_answer', 'essay', 'matching', 'ordering')
difficulty_level: ENUM('Easy', 'Medium', 'Hard')
curriculum_node_id: FK → curriculum_nodes
bloom_level: ENUM (as above)
correct_answer: VARCHAR/TEXT
explanation: TEXT
tags: TEXT[] (for categorization)
statistics: JSONB {
  pass_rate: DECIMAL,
  avg_time_seconds: INT,
  discrimination_index: DECIMAL,
  p_value: DECIMAL
}
created_by: FK → teachers
created_at: TIMESTAMP
```

#### NEW: LEARNING_PROFILE
```sql
id: UUID (PK)
student_id: FK → students
learning_style: ENUM('visual', 'auditory', 'kinesthetic')
learning_pace: ENUM('slow', 'medium', 'fast')
preferred_quest_difficulty: ENUM('Easy', 'Medium', 'Hard')
timezone: VARCHAR
notifications_enabled: BOOLEAN
preferred_language: VARCHAR
dark_mode: BOOLEAN
```

#### NEW: STUDY_GROUP
```sql
id: UUID (PK)
name: VARCHAR
description: TEXT
owner_id: FK → students
curriculum_focus_node: FK → curriculum_nodes
created_at: TIMESTAMP
is_active: BOOLEAN
max_members: INT
shared_quest_id: FK → quests
```

---

## 3. API Specifications (RESTful + WebSocket)

### 3.1 Authentication Service

#### POST /auth/register
```json
Request:
{
  "national_id": "060315..." ,
  "first_name": "Thandi",
  "email": "thandi@school.edu.za",
  "password": "secure_password",
  "grade_level": 10
}

Response (201):
{
  "user_id": "uuid",
  "access_token": "jwt_token",
  "refresh_token": "jwt_token"
}
```

#### POST /auth/login
```json
Request:
{
  "email": "thandi@school.edu.za",
  "password": "password"
}

Response (200):
{
  "access_token": "jwt",
  "user_id": "uuid",
  "role": "student"
}
```

### 3.2 Gap Detection & Quest Service

#### GET /gaps/analyze/{student_id}
```json
Response (200):
{
  "student_id": "uuid",
  "critical_gaps": [
    {
      "concept": "Algebraic Expressions",
      "mastery_score": 0.35,
      "severity": 5,
      "recommended_action": "Start Boss Battle"
    }
  ],
  "boss_battles": [
    {
      "quest_id": "uuid",
      "concept": "Algebraic Expressions",
      "boss_name": "The Expression Guardian",
      "objectives": [...],
      "difficulty": "Hard",
      "reward_points": 750
    }
  ]
}
```

### 3.3 AI Tutoring Service

#### POST /tutor/ask
```json
Request:
{
  "student_id": "uuid",
  "question": "How do I solve 2x + 5 = 13?",
  "curriculum_node_id": "uuid",
  "difficulty_level": "beginner"  // override
}

Response (200):
{
  "response": "Let's work through this step by...",
  "steps": [
    {"step": 1, "explanation": "..."},
    {"step": 2, "explanation": "..."}
  ],
  "multiple_explanations": {
    "eli5": "Think of it like...",
    "advanced": "Using algebraic manipulation..."
  },
  "related_topics": [...]
}
```

### 3.4 Leaderboard Service

#### GET /leaderboards/{type}/{period}
```json
Params:
  type: 'subject' | 'school' | 'national' | 'skill'
  period: 'daily' | 'weekly' | 'monthly' | 'all_time'
  limit: 100

Response (200):
{
  "type": "subject",
  "subject": "Mathematics",
  "period": "weekly",
  "entries": [
    {
      "rank": 1,
      "student_id": "uuid",
      "student_name": "Thandi Mkhize",
      "school": "Northwich Academy",
      "points": 2500,
      "mastery_score": 0.92,
      "achievements_earned": 3
    },
    ...
  ],
  "generated_at": "2026-03-19T10:00:00Z"
}
```

### 3.5 Analytics Dashboard Service

#### GET /dashboard/class/{teacher_id}
```json
Response (200):
{
  "class_id": "uuid",
  "class_name": "10A Mathematics",
  "students_total": 35,
  "mastery_overview": {
    "topics": [
      {
        "topic": "Algebraic Expressions",
        "avg_mastery": 0.62,
        "mastered_count": 12,
        "at_risk_count": 8
      }
    ]
  },
  "at_risk_students": [
    {
      "student_id": "uuid",
      "name": "Sipho Mthembu",
      "risk_score": 0.92,
      "reason": "Declining trend in Math",
      "recommendation": "Extra tutoring session recommended"
    }
  ],
  "engagement_stats": {...}
}
```

### 3.6 Prediction Service

#### GET /predict/risk/{student_id}
```json
Response (200):
{
  "student_id": "uuid",
  "failure_probability": 0.87,
  "confidence": 0.94,
  "risk_factors": [
    "Low mastery in prerequisites",
    "Declining engagement",
    "High attempt count without improvement"
  ],
  "recommended_interventions": [
    "Increase AI tutoring sessions",
    "Assign to study group",
    "Give motivational quest"
  ]
}
```

### 3.7 WebSocket: Real-Time Collaboration

#### WS /collaborate/{session_id}
```
Message Types:
- PROBLEM_SOLVE: Share step on shared problem
- WHITEBOARD_UPDATE: Draw on shared whiteboard
- CHAT: Text message
- VOICE_SIGNAL: WebRTC signaling for voice/video
- PRESENCE: User joined/left
- CURSOR: Shared cursor position

Example Message:
{
  "type": "PROBLEM_SOLVE",
  "student_id": "uuid",
  "step": "2x = 8",
  "reasoning": "Subtract 5 from both sides",
  "timestamp": 1234567890
}
```

---

## 4. AI/ML Specifications

### 4.1 Gap Detection Algorithm
```
Input: student_id, mastery_scores[]
Output: critical_gaps[], boss_battles[]

1. Filter nodes where mastery < THRESHOLD (0.5)
2. For each gap:
   a. Identify gap_type (foundational/prerequisite/core)
   b. Calculate severity (1-5 based on impact)
   c. Check if foundational → trigger_boss_battle()
3. Generate quest objectives:
   a. Extract learning outcomes from curriculum
   b. Break down into 4-6 measurable objectives
   c. Set difficulty = 'Hard'
4. Calculate reward_points = 500 + (severity * 100)
```

### 4.2 Predictive Failure Model
```
Features:
- mastery_score_trajectory (recent slope)
- engagement_score (time on task, activity frequency)
- attempt_count_without_improvement
- prerequisite_gap_count
- time_since_last_assessment
- peer_comparison (z-score within class)

Model: Random Forest or XGBoost
Training Data: Historical student outcomes
Target: Binary (fail/pass at term end)
Validation: 5-fold cross-validation
Threshold: Predict "at-risk" if p(fail) > 0.7
```

### 4.3 Spaced Repetition Algorithm
```
Based on: Leitner System / SuperMemo SM-2

1. Student completes assessment
2. Score determines "bin" (1-5):
   Bin 1: Easy     → review in 1 day
   Bin 2: Good     → review in 3 days
   Bin 3: Medium   → review in 7 days
   Bin 4: Hard     → review in 14 days
   Bin 5: Struggle → review in 1 day + extra tutoring

3. Calculate effectiveness factor (EF)
   EF = EF_prev + (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02))

4. Calculate next interval
   interval = interval_prev * EF

5. Trigger notification for review
```

### 4.4 Learning Style Adaptation
```
Assessment Phase (Initial):
- 10-question learning style assessment (VARK-style)
- Determine: Visual | Auditory | Kinesthetic | Mixed

Content Delivery:
- Visual Learners: Diagrams, mind maps, video explanations
- Auditory Learners: Podcasts, narration, verbal explanations
- Kinesthetic Learners: Interactive simulations, labs, hands-on practices

Tracking:
- Monitor quiz performance by content type
- Adjust mix if performance improves with certain style
```

---

## 5. Security Specifications

### 5.1 Authentication & Authorization

#### JWT Tokens
```
Access Token:
- Expiry: 1 hour
- Payload: {user_id, role, email, grade_level}
- Secret: Environment variable

Refresh Token:
- Expiry: 30 days
- Payload: {user_id, issued_at}
- Stored in secure HTTP-only cookie

Roles:
- student
- teacher
- school_admin
- national_admin
```

#### OAuth2 Integration
```
Providers to support: 
- Google Edu
- Microsoft 365 (for schools)

Flow: Authorization Code Grant
```

### 5.2 Data Encryption
```
Encryption at rest:
- Database: AES-256 for sensitive fields (national_id, email)
- Files: AES-256 for uploaded documents

Encryption in transit:
- TLS 1.3 for all HTTPS
- WSS (WebSocket Secure) for real-time

Key management:
- AWS KMS or HashiCorp Vault
- Rotate keys quarterly
```

### 5.3 Compliance

#### POPIA (Protection of Personal Information Act - South Africa)
- Consent before data collection: ✓
- Purpose limitation: ✓
- Security measures: ✓
- Right to access: ✓
- Data deletion (right to be forgotten): ✓
- Privacy by design: ✓
- Data Protection Officer (role): ✓

#### Data Retention
```
Students (inactive):
- Keep 2 years then anonymize

Assessment Results:
- Keep 5 years (academic records)

Logs:
- Keep 90 days (security/debugging)
- Archive to cold storage for 2 years
```

---

## 6. Performance Specifications

### 6.1 API Performance Targets

| Endpoint | Target (p95) | Target (p99) |
|----------|------------|------------|
| GET /health | 10ms | 20ms |
| POST /auth/login | 100ms | 200ms |
| GET /gaps/analyze | 500ms | 1000ms |
| GET /tutor/ask | 2000ms | 5000ms (API latency) |
| GET /leaderboards | 200ms | 500ms |
| GET /dashboard/class | 1000ms | 2000ms |
| WS /collaborate | <50ms message | <100ms |

### 6.2 Database Performance

```sql
-- Index Strategy
CREATE INDEX idx_students_is_active ON students(is_active);
CREATE INDEX idx_mastery_student_node ON mastery_graph(student_id, curriculum_node_id);
CREATE INDEX idx_results_student_date ON assessment_results(student_id, attempted_at);
CREATE INDEX idx_leaderboard_period_type ON leaderboard_entry(period, leaderboard_type, rank);

-- Query optimization
- Avoid N+1 queries (use SQL JOINs)
- Implement materialized views for leaderboards
- Use connection pooling (pgBouncer)
```

### 6.3 Caching Strategy

```
Redis Key Patterns:
- leaderboard:{type}:{period} → JSON (expire: 1 hour)
- student_profile:{student_id} → JSON (expire: 24 hours)
- curriculum_topics → JSON (expire: 7 days)
- ai_cache:{hash(question)} → cached response (expire: 30 days)

Cache Invalidation:
- On assessment result → invalidate leaderboards
- On data update → invalidate student_profile
- Scheduled: Rebuild leaderboards every 1 hour
```

---

## 7. Scalability Specifications

### 7.1 Horizontal Scaling

```
Load Balancing:
- Nginx reverse proxy
- Round-robin or least-connections strategy

API Servers:
- Stateless FastAPI instances
- Auto-scaling group: 5-100 instances (based on CPU/memory)
- Container orchestration: Kubernetes

Database:
- Primary-replica setup for read scaling
- Connection pooling: 500-1000 connections
- Sharding strategy (if needed): by school_id
```

### 7.2 Capacity Planning

| Load | Concurrent Users | QPS | Required Instances |
|------|-----------------|-----|-------------------|
| Light | 1,000 | 100 | 2-3 API + 1 DB |
| Medium | 10,000 | 1,000 | 5-10 API + 2 DB |
| Heavy | 50,000 | 5,000 | 20-30 API + 4 DB |
| Peak | 100,000 | 10,000 | 50-100 API + 8 DB |

---

## 8. Monitoring & Observability

### 8.1 Metrics to Track

```
Application:
- Request latency (p50, p95, p99)
- Error rate (4xx, 5xx)
- API endpoint usage
- Cache hit rate

Business:
- MAU (Monthly Active Users)
- Student mastery improvement
- Engagement (time on task)
- Feature adoption rates

Infrastructure:
- CPU/memory utilization
- Disk I/O
- Network bandwidth
- Database query time
```

### 8.2 Logging & Error Tracking

```
Tool: ELK Stack + Sentry

Logs to capture:
- API requests/responses
- Authentication events
- Data mutations
- Errors & exceptions
- User actions (for audit trail)

Retention: 90 days hot, 2 years cold archive
```

---

## 9. Deployment Specifications

### 9.1 Environment Strategy

```
Development:
- Local SQLite for fast iteration
- Mock OpenAI API
- Single FastAPI instance

Staging:
- PostgreSQL (replica of production schema)
- Real OpenAI API (limited key)
- Multi-instance setup
- Staging database seeded with sanitized production data

Production:
- PostgreSQL with replication
- Real OpenAI API (full access)
- Multi-region deployment (if needed)
- Automated backups (hourly snapshots)
```

### 9.2 Deployment Pipeline

```
Git → GitHub Actions → Docker Build → Registry → K8s Deploy

Steps:
1. Lint & format check
2. Unit tests (>80% coverage)
3. Integration tests
4. Build Docker image
5. Push to registry
6. Deploy to staging
7. Smoke tests
8. Approval gate
9. Deploy to production
10. Health checks
```

---

## 10. Integration Points

### External APIs
```
OpenAI (ChatGPT/GPT-4):
- Endpoint: https://api.openai.com/v1/chat/completions
- Rate limit: 3,500 RPM (on demand plan)
- Cost: $0.03-$0.06 per 1K tokens

NLP/Tagging:
- spaCy for natural language processing
- Self-hosted or API service

Video Streaming (Future):
- Vimeo or self-hosted HLS server
- Adaptive bitrate streaming

Video Conferencing (Future):
- Twilio or Agora for WebRTC
- Recording support
```

---

## 11. Testing Specifications

### 11.1 Test Coverage Targets

| Type | Target | Purpose |
|------|--------|---------|
| Unit | >80% | Individual functions |
| Integration | >60% | API endpoints |
| E2E | >40% | Key user flows |
| Load | 10k concurrent | Stress testing |

### 11.2 Test Scenarios

```python
# Gap Detection Tests
test_identify_gap_below_threshold()
test_no_gap_above_threshold()
test_multi_gap_analysis()
test_boss_battle_generation()

# Leaderboard Tests
test_ranking_calculation()
test_period_filtering()
test_concurrent_updates()

# Prediction Tests
test_failure_prediction_accuracy()
test_false_positive_rate()
test_recommendation_quality()

# Load Tests
test_10k_concurrent_reads()
test_1k_concurrent_writes()
test_api_latency_under_load()
```

---

## 12. Roadmap for Implementation

| Phase | System Component | Delivery |
|-------|-----------------|----------|
| 1 | Gap Detection, Boss Battles | ✓ Complete |
| 2 | Leaderboards, Achievements | Week 5-8 |
| 3 | AI Tutoring, Predictive Model | Week 9-14 |
| 4 | Multi-grade, Mobile, i18n | Week 15-20 |
| 5 | Assessment Bank, Adaptive Testing | Week 21-26 |
| 6 | Real-time Collab, Advanced Features | Week 27-32 |

---

## 13. Success Metrics

**Technical Success**:
- API response time p95 < 500ms
- System availability > 99.5%
- Test coverage > 80%
- Zero data loss incidents

**Product Success**:
- 50,000+ active students by EOY
- 70%+ mastery improvement in identified gaps
- 60%+ student engagement rate
- 80%+ teacher satisfaction

---

*Technical Specifications Last Updated: March 2026*
*Status: ACTIVE DEVELOPMENT*
