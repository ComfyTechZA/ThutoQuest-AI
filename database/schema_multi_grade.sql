-- ThutoQuest-AI Multi-Grade Mastery Tracker Schema (Grades R-12)
-- PostgreSQL database schema for tracking student mastery across South African CAPS curriculum
-- Includes Offline-First sync capabilities

-- Enable UUID and JSON extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- ENUMS & TYPES
-- ============================================================================

CREATE TYPE grade_level AS ENUM (
    'R', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'
);

CREATE TYPE subject_type AS ENUM (
    'Mathematics',
    'Science',
    'English',
    'Afrikaans',
    'Xhosa',
    'Zulu',
    'Sotho',
    'History',
    'Geography',
    'Life_Orientation',
    'Technology',
    'Art',
    'Music',
    'Physical_Education'
);

CREATE TYPE mastery_status AS ENUM (
    'Not Started',
    'In Progress',
    'Completed',
    'Mastered'
);

CREATE TYPE sync_status AS ENUM (
    'pending',
    'synced',
    'conflict',
    'failed'
);

CREATE TYPE operation_type AS ENUM (
    'INSERT',
    'UPDATE',
    'DELETE'
);

-- ============================================================================
-- CORE TABLES
-- ============================================================================

-- SCHOOLS TABLE
CREATE TABLE schools (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    district VARCHAR(255),
    province VARCHAR(100) NOT NULL,
    country VARCHAR(100) DEFAULT 'South Africa',
    email VARCHAR(255),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- STUDENTS TABLE (Multi-grade)
CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    national_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    current_grade grade_level NOT NULL,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    date_of_birth DATE,
    gender VARCHAR(20),
    home_language VARCHAR(50),
    learning_style VARCHAR(50) DEFAULT 'visual',
    avatar_id UUID,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    is_offline_enabled BOOLEAN DEFAULT FALSE,
    last_sync_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_national_id CHECK (national_id ~ '^\d{13}$')
);

-- TEACHERS TABLE
CREATE TABLE teachers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    national_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    specialization VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TEACHER_CLASS ASSIGNMENTS
CREATE TABLE teacher_classes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    teacher_id UUID NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    class_name VARCHAR(50) NOT NULL,
    grade grade_level NOT NULL,
    subject subject_type NOT NULL,
    student_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(teacher_id, class_name, grade, subject)
);

-- STUDENT_CLASS ENROLLMENT
CREATE TABLE student_class_enrollment (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    class_id UUID NOT NULL REFERENCES teacher_classes(id) ON DELETE CASCADE,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    UNIQUE(student_id, class_id)
);

-- CURRICULUM NODES (CAPS Aligned, Multi-Grade)
CREATE TABLE curriculum_nodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subject subject_type NOT NULL,
    grade grade_level NOT NULL,
    topic_name VARCHAR(500) NOT NULL,
    description TEXT,
    learning_outcomes TEXT,
    assessment_standards TEXT,
    estimated_hours INT,
    difficulty_level VARCHAR(20) CHECK (difficulty_level IN ('Easy', 'Medium', 'Hard')),
    bloom_level VARCHAR(50) CHECK (bloom_level IN ('Remember', 'Understand', 'Apply', 'Analyze', 'Evaluate', 'Create')),
    prerequisite_node_id UUID REFERENCES curriculum_nodes(id) ON DELETE SET NULL,
    parent_unit_id UUID REFERENCES curriculum_nodes(id) ON DELETE SET NULL,
    caps_reference VARCHAR(255),
    sort_order INT,
    resource_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(subject, grade, topic_name)
);

-- MASTERY GRAPH (Multi-Grade, Offline-Aware)
CREATE TABLE mastery_graph (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    curriculum_node_id UUID NOT NULL REFERENCES curriculum_nodes(id) ON DELETE CASCADE,
    mastery_score DECIMAL(3, 2) NOT NULL DEFAULT 0.0 CHECK (mastery_score >= 0.0 AND mastery_score <= 1.0),
    confidence_interval DECIMAL(4, 3),
    last_assessment_date TIMESTAMP,
    number_of_attempts INT DEFAULT 0,
    time_spent_minutes INT DEFAULT 0,
    is_mastered BOOLEAN GENERATED ALWAYS AS (mastery_score >= 0.8) STORED,
    status mastery_status DEFAULT 'Not Started',
    retention_score DECIMAL(3, 2),
    next_review_date TIMESTAMP,
    notes TEXT,
    is_synced BOOLEAN DEFAULT FALSE,
    local_version INT DEFAULT 0,
    remote_version INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_student_node UNIQUE(student_id, curriculum_node_id)
);

-- ASSESSMENT RESULTS (Multi-Grade)
CREATE TABLE assessment_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    mastery_graph_id UUID NOT NULL REFERENCES mastery_graph(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    curriculum_node_id UUID NOT NULL REFERENCES curriculum_nodes(id) ON DELETE CASCADE,
    score DECIMAL(3, 2) NOT NULL CHECK (score >= 0.0 AND score <= 1.0),
    questions_correct INT,
    questions_total INT,
    assessment_type VARCHAR(50) CHECK (assessment_type IN ('Quiz', 'Test', 'Assignment', 'Project', 'Adaptive', 'Diagnostic')),
    item_ids UUID[],
    time_spent_seconds INT,
    difficulty_presented VARCHAR(20),
    adaptive_level_adjusted BOOLEAN,
    item_response_theory_theta DECIMAL(5, 3),
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_synced BOOLEAN DEFAULT FALSE,
    local_version INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_results_student_date (student_id, attempted_at)
);

-- ============================================================================
-- GAMIFICATION TABLES
-- ============================================================================

-- ACHIEVEMENTS & BADGES
CREATE TABLE achievements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    achievement_key VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    icon_url VARCHAR(500),
    rarity VARCHAR(50) CHECK (rarity IN ('Common', 'Uncommon', 'Rare', 'Epic', 'Legendary')),
    unlock_condition JSONB,
    points_reward INT DEFAULT 100,
    grade_applicable grade_level[] DEFAULT ARRAY['1','2','3','4','5','6','7','8','9','10','11','12'],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- STUDENT ACHIEVEMENTS
CREATE TABLE student_achievements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    achievement_id UUID NOT NULL REFERENCES achievements(id) ON DELETE CASCADE,
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_synced BOOLEAN DEFAULT FALSE,
    UNIQUE(student_id, achievement_id)
);

-- LEADERBOARDS
CREATE TABLE leaderboard_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    leaderboard_type VARCHAR(50) CHECK (leaderboard_type IN ('subject', 'school', 'provincial', 'national', 'skill', 'grade')),
    period VARCHAR(50) CHECK (period IN ('daily', 'weekly', 'monthly', 'term', 'all_time')),
    grade grade_level,
    subject subject_type,
    rank INT,
    score INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_leaderboard (leaderboard_type, period, rank)
);

-- ============================================================================
-- OFFLINE-FIRST SYNC TABLES
-- ============================================================================

-- SYNC LOG (For Offline-First Architecture)
CREATE TABLE sync_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    operation operation_type NOT NULL,
    local_data JSONB NOT NULL,
    remote_data JSONB,
    status sync_status DEFAULT 'pending',
    sync_timestamp TIMESTAMP,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT,
    conflict_resolution VARCHAR(100) CHECK (conflict_resolution IN ('local_wins', 'remote_wins', 'merged', 'manual')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SYNC QUEUE (For reliable offline-first sync)
CREATE TABLE sync_queue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    operation operation_type NOT NULL,
    payload JSONB NOT NULL,
    priority INT DEFAULT 0,
    status sync_status DEFAULT 'pending',
    retry_count INT DEFAULT 0,
    max_retries INT DEFAULT 3,
    last_retry_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_sync_queue_status (status, priority, created_at)
);

-- DEVICE REGISTRY (Track offline devices for sync)
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    device_id VARCHAR(255) NOT NULL,
    device_type VARCHAR(50) CHECK (device_type IN ('mobile', 'tablet', 'web')),
    platform VARCHAR(50) CHECK (platform IN ('iOS', 'Android', 'Web')),
    app_version VARCHAR(20),
    last_sync_at TIMESTAMP,
    is_online BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, device_id)
);

-- ============================================================================
-- ANALYTICS & INSIGHTS TABLES
-- ============================================================================

-- LEARNING PROFILE
CREATE TABLE learning_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL UNIQUE REFERENCES students(id) ON DELETE CASCADE,
    learning_style VARCHAR(50),
    learning_pace VARCHAR(50) CHECK (learning_pace IN ('slow', 'medium', 'fast')),
    preferred_difficulty VARCHAR(20),
    timezone VARCHAR(100),
    notifications_enabled BOOLEAN DEFAULT TRUE,
    dark_mode BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- PREDICTIVE RISK SCORES (For AI interventions)
CREATE TABLE risk_predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    curriculum_node_id UUID NOT NULL REFERENCES curriculum_nodes(id) ON DELETE CASCADE,
    failure_probability DECIMAL(3, 2),
    confidence_level DECIMAL(3, 2),
    risk_factors JSONB,
    recommended_interventions JSONB,
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    outcome_date TIMESTAMP,
    actual_outcome VARCHAR(50),
    model_accuracy DECIMAL(3, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- STUDY GROUPS (Collaborative Learning)
CREATE TABLE study_groups (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    curriculum_node_id UUID REFERENCES curriculum_nodes(id) ON DELETE SET NULL,
    school_id UUID NOT NULL REFERENCES schools(id) ON DELETE CASCADE,
    grade grade_level,
    max_members INT DEFAULT 10,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- GROUP MEMBERSHIP
CREATE TABLE group_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    group_id UUID NOT NULL REFERENCES study_groups(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(group_id, student_id)
);

-- ============================================================================
-- AUDIT & COMPLIANCE TABLES
-- ============================================================================

-- AUDIT LOG
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(10) CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values JSONB,
    new_values JSONB,
    changed_by UUID,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DATA ACCESS LOG (For POPIA compliance)
CREATE TABLE data_access_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    access_type VARCHAR(50) CHECK (access_type IN ('view', 'edit', 'delete', 'export')),
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- ============================================================================

-- Students
CREATE INDEX idx_students_national_id ON students(national_id);
CREATE INDEX idx_students_school_id ON students(school_id);
CREATE INDEX idx_students_is_active ON students(is_active);
CREATE INDEX idx_students_grade ON students(current_grade);

-- Curriculum Nodes
CREATE INDEX idx_curriculum_subject_grade ON curriculum_nodes(subject, grade);
CREATE INDEX idx_curriculum_grade ON curriculum_nodes(grade);
CREATE INDEX idx_curriculum_parent ON curriculum_nodes(parent_unit_id);
CREATE INDEX idx_curriculum_subject ON curriculum_nodes(subject);

-- Mastery Graph
CREATE INDEX idx_mastery_student ON mastery_graph(student_id);
CREATE INDEX idx_mastery_node ON mastery_graph(curriculum_node_id);
CREATE INDEX idx_mastery_status ON mastery_graph(status);
CREATE INDEX idx_mastery_is_mastered ON mastery_graph(is_mastered);
CREATE INDEX idx_mastery_student_node ON mastery_graph(student_id, curriculum_node_id);
CREATE INDEX idx_mastery_not_synced ON mastery_graph(is_synced) WHERE NOT is_synced;

-- Assessment Results
CREATE INDEX idx_assessment_student ON assessment_results(student_id);
CREATE INDEX idx_assessment_node ON assessment_results(curriculum_node_id);
CREATE INDEX idx_assessment_date ON assessment_results(attempted_at);

-- Sync Log
CREATE INDEX idx_sync_log_student ON sync_log(student_id);
CREATE INDEX idx_sync_log_status ON sync_log(status);
CREATE INDEX idx_sync_log_pending ON sync_log(status) WHERE status = 'pending';

-- Achievements
CREATE INDEX idx_student_achievements ON student_achievements(student_id);

-- ============================================================================
-- VIEWS FOR ANALYTICS
-- ============================================================================

-- Student Progress Summary
CREATE VIEW vw_student_progress_summary AS
SELECT 
    s.id,
    s.national_id,
    s.first_name,
    s.last_name,
    s.current_grade,
    sch.name AS school_name,
    COUNT(DISTINCT mg.curriculum_node_id) as total_nodes,
    COUNT(DISTINCT CASE WHEN mg.is_mastered THEN mg.curriculum_node_id END) as mastered_nodes,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN mg.is_mastered THEN mg.curriculum_node_id END) / 
        NULLIF(COUNT(DISTINCT mg.curriculum_node_id), 0), 2) as mastery_percentage,
    AVG(mg.mastery_score) as average_mastery_score,
    MAX(mg.last_assessment_date) as last_assessment_date,
    COUNT(DISTINCT CASE WHEN mg.status = 'In Progress' THEN mg.curriculum_node_id END) as in_progress_count
FROM students s
LEFT JOIN mastery_graph mg ON s.id = mg.student_id
LEFT JOIN schools sch ON s.school_id = sch.id
WHERE s.is_active = TRUE
GROUP BY s.id, s.national_id, s.first_name, s.last_name, s.current_grade, sch.name;

-- Curriculum Node Statistics
CREATE VIEW vw_curriculum_node_statistics AS
SELECT 
    cn.id,
    cn.subject,
    cn.grade,
    cn.topic_name,
    cn.difficulty_level,
    COUNT(DISTINCT mg.student_id) as total_students_assigned,
    COUNT(DISTINCT CASE WHEN mg.is_mastered THEN mg.student_id END) as students_mastered,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN mg.is_mastered THEN mg.student_id END) / 
        NULLIF(COUNT(DISTINCT mg.student_id), 0), 2) as mastery_rate,
    AVG(mg.mastery_score) as average_mastery_score,
    AVG(mg.time_spent_minutes) as average_time_spent
FROM curriculum_nodes cn
LEFT JOIN mastery_graph mg ON cn.id = mg.curriculum_node_id
WHERE cn.is_active = TRUE
GROUP BY cn.id, cn.subject, cn.grade, cn.topic_name, cn.difficulty_level;

-- School Performance Overview
CREATE VIEW vw_school_performance AS
SELECT 
    sch.id,
    sch.name,
    sch.district,
    COUNT(DISTINCT s.id) as total_students,
    COUNT(DISTINCT CASE WHEN s.is_active = TRUE THEN s.id END) as active_students,
    ROUND(AVG(mg.mastery_score), 2) as avg_school_mastery,
    COUNT(DISTINCT CASE WHEN mg.is_mastered THEN mg.student_id END) as total_mastered_nodes,
    COUNT(DISTINCT tc.id) as total_classes
FROM schools sch
LEFT JOIN students s ON sch.id = s.school_id
LEFT JOIN mastery_graph mg ON s.id = mg.student_id
LEFT JOIN teacher_classes tc ON sch.id = tc.school_id
GROUP BY sch.id, sch.name, sch.district;

-- Offline Sync Status
CREATE VIEW vw_sync_status AS
SELECT 
    student_id,
    COUNT(*) as total_pending,
    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_count,
    SUM(CASE WHEN status = 'synced' THEN 1 ELSE 0 END) as synced_count,
    SUM(CASE WHEN status = 'conflict' THEN 1 ELSE 0 END) as conflict_count,
    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_count,
    MAX(created_at) as last_sync_attempt
FROM sync_log
GROUP BY student_id;

-- ============================================================================
-- STORED PROCEDURES FOR COMMON OPERATIONS
-- ============================================================================

-- Calculate Mastery Score Based on Assessments
CREATE OR REPLACE FUNCTION calculate_mastery_score(
    p_student_id UUID,
    p_node_id UUID
)
RETURNS DECIMAL AS $$
DECLARE
    v_score DECIMAL;
BEGIN
    SELECT AVG(score) INTO v_score
    FROM assessment_results
    WHERE student_id = p_student_id
    AND curriculum_node_id = p_node_id
    AND attempted_at > CURRENT_TIMESTAMP - INTERVAL '90 days';
    
    RETURN COALESCE(v_score, 0.0);
END;
$$ LANGUAGE plpgsql;

-- Queue a Sync Operation
CREATE OR REPLACE FUNCTION queue_sync_operation(
    p_student_id UUID,
    p_table_name VARCHAR,
    p_record_id UUID,
    p_operation operation_type,
    p_payload JSONB
)
RETURNS UUID AS $$
DECLARE
    v_sync_id UUID;
BEGIN
    INSERT INTO sync_queue (student_id, table_name, record_id, operation, payload)
    VALUES (p_student_id, p_table_name, p_record_id, p_operation, p_payload)
    RETURNING id INTO v_sync_id;
    
    RETURN v_sync_id;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================

-- Schema Version
COMMENT ON SCHEMA public IS 'ThutoQuest-AI Multi-Grade Mastery Tracker Schema v2.0 - Supports Grades R-12 with Offline-First Sync';
