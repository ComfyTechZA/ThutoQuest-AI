-- ThutoQuest-AI Grade 10 Mastery Tracker Schema
-- PostgreSQL database schema for tracking student mastery of curriculum nodes

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Students Table
CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    national_id VARCHAR(20) UNIQUE NOT NULL COMMENT 'Unique national ID for student',
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    grade_level INTEGER NOT NULL DEFAULT 10,
    school_name VARCHAR(255),
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_grade_level CHECK (grade_level = 10)
);

-- Curriculum Nodes Table
CREATE TABLE curriculum_nodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subject VARCHAR(50) NOT NULL CHECK (subject IN ('Mathematics', 'Science')),
    topic_name VARCHAR(255) NOT NULL,
    description TEXT,
    grade_level INTEGER NOT NULL DEFAULT 10,
    learning_outcomes TEXT,
    estimated_hours INTEGER,
    difficulty_level VARCHAR(20) CHECK (difficulty_level IN ('Easy', 'Medium', 'Hard')),
    prerequisite_node_id UUID REFERENCES curriculum_nodes(id) ON DELETE SET NULL,
    parent_unit_id UUID REFERENCES curriculum_nodes(id) ON DELETE SET NULL,
    sort_order INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(subject, topic_name, grade_level)
);

-- Mastery Graph Table
-- Tracks student progress on each curriculum node
CREATE TABLE mastery_graph (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    curriculum_node_id UUID NOT NULL REFERENCES curriculum_nodes(id) ON DELETE CASCADE,
    mastery_score DECIMAL(3, 2) NOT NULL DEFAULT 0.0 CHECK (mastery_score >= 0.0 AND mastery_score <= 1.0),
    last_assessment_date TIMESTAMP,
    number_of_attempts INTEGER DEFAULT 0,
    time_spent_minutes INTEGER DEFAULT 0,
    is_mastered BOOLEAN GENERATED ALWAYS AS (mastery_score >= 0.8) STORED,
    status VARCHAR(20) DEFAULT 'Not Started' CHECK (status IN ('Not Started', 'In Progress', 'Completed', 'Mastered')),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_student_node UNIQUE(student_id, curriculum_node_id)
);

-- Assessment Results Table (optional but useful for tracking detailed assessment history)
CREATE TABLE assessment_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    mastery_graph_id UUID NOT NULL REFERENCES mastery_graph(id) ON DELETE CASCADE,
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    curriculum_node_id UUID NOT NULL REFERENCES curriculum_nodes(id) ON DELETE CASCADE,
    score DECIMAL(3, 2) NOT NULL CHECK (score >= 0.0 AND score <= 1.0),
    questions_correct INTEGER,
    questions_total INTEGER,
    assessment_type VARCHAR(50) CHECK (assessment_type IN ('Quiz', 'Test', 'Assignment', 'Project')),
    time_spent_seconds INTEGER,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance optimization
CREATE INDEX idx_students_national_id ON students(national_id);
CREATE INDEX idx_students_is_active ON students(is_active);
CREATE INDEX idx_curriculum_nodes_subject ON curriculum_nodes(subject);
CREATE INDEX idx_curriculum_nodes_grade_level ON curriculum_nodes(grade_level);
CREATE INDEX idx_curriculum_nodes_parent ON curriculum_nodes(parent_unit_id);
CREATE INDEX idx_mastery_graph_student ON mastery_graph(student_id);
CREATE INDEX idx_mastery_graph_node ON mastery_graph(curriculum_node_id);
CREATE INDEX idx_mastery_graph_status ON mastery_graph(status);
CREATE INDEX idx_mastery_graph_is_mastered ON mastery_graph(is_mastered);
CREATE INDEX idx_mastery_graph_student_node ON mastery_graph(student_id, curriculum_node_id);
CREATE INDEX idx_assessment_results_mastery_graph ON assessment_results(mastery_graph_id);
CREATE INDEX idx_assessment_results_student ON assessment_results(student_id);
CREATE INDEX idx_assessment_results_node ON assessment_results(curriculum_node_id);

-- Audit Trail Table
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name VARCHAR(100) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(10) CHECK (action IN ('INSERT', 'UPDATE', 'DELETE')),
    old_values JSONB,
    new_values JSONB,
    changed_by VARCHAR(255),
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- View for student progress summary
CREATE VIEW vw_student_progress_summary AS
SELECT 
    s.id,
    s.national_id,
    s.first_name,
    s.last_name,
    s.email,
    COUNT(DISTINCT mg.curriculum_node_id) as total_nodes,
    COUNT(DISTINCT CASE WHEN mg.is_mastered THEN mg.curriculum_node_id END) as mastered_nodes,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN mg.is_mastered THEN mg.curriculum_node_id END) / 
        NULLIF(COUNT(DISTINCT mg.curriculum_node_id), 0), 2) as mastery_percentage,
    AVG(mg.mastery_score) as average_mastery_score,
    MAX(mg.last_assessment_date) as last_assessment_date,
    COUNT(DISTINCT CASE WHEN mg.status = 'In Progress' THEN mg.curriculum_node_id END) as in_progress_count
FROM students s
LEFT JOIN mastery_graph mg ON s.id = mg.student_id
WHERE s.is_active = TRUE
GROUP BY s.id, s.national_id, s.first_name, s.last_name, s.email;

-- View for curriculum node statistics
CREATE VIEW vw_curriculum_node_statistics AS
SELECT 
    cn.id,
    cn.subject,
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
GROUP BY cn.id, cn.subject, cn.topic_name, cn.difficulty_level;
