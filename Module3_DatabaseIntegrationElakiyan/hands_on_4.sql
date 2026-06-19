USE college_db;


-- Task 1: Baseline Performance - No Indexes


-- Baseline EXPLAIN plan
EXPLAIN FORMAT=JSON
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

--  Identify full table scans (check EXPLAIN output)
-- Note rows examined / estimated cost in comments


-- Task 2: Add Indexes and Compare Plans


-- B-Tree index on students.enrollment_year
CREATE INDEX idx_students_enrollment_year ON students(enrollment_year);

--  Composite UNIQUE index on enrollments(student_id, course_id)
CREATE UNIQUE INDEX idx_enrollments_student_course ON enrollments(student_id, course_id);

-- Index on courses.course_code
CREATE INDEX idx_courses_code ON courses(course_code);

-- Re-run EXPLAIN after indexes
EXPLAIN FORMAT=JSON
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
WHERE s.enrollment_year = 2022;

-- 55. Partial index (PostgreSQL only; MySQL ignores WHERE in index)
--For MySQL, simulate with filtered queries
CREATE INDEX idx_enrollments_null_grades ON enrollments(student_id) WHERE grade IS NULL;

--
-- Task 3: Identify and Fix the N+1 Problem
-- 

-- Simulate N+1 problem in Python (pseudo-code)
SELECT * FROM enrollments;
For each row: SELECT student_name FROM students WHERE student_id = ?;

-- Fix with JOIN query
SELECT e.enrollment_id, s.first_name, s.last_name, c.course_name, e.grade
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id;


