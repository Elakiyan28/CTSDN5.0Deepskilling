USE college_db;


-- Task 1: Insert, Update, Delete


-- Insert two additional students
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year)
VALUES ('Rahul', 'Sharma', 'rahul.sharma@college.edu', '2003-12-05', 1, 2022),
       ('Neha', 'Kapoor', 'neha.kapoor@college.edu', '2004-02-18', 2, 2023);

-- Update grade for student_id=5, course_id=1 from 'C' to 'B'
UPDATE enrollments
SET grade = 'B'
WHERE student_id = 5 AND course_id = 1;

-- Delete enrollments where grade IS NULL
DELETE FROM enrollments WHERE grade IS NULL;

-- Verify row counts
SELECT COUNT(*) AS total_students FROM students;
SELECT COUNT(*) AS total_enrollments FROM enrollments;

-- Task 2: Single-Table Queries

-- Students enrolled in 2022, ordered by last_name
SELECT * FROM students WHERE enrollment_year = 2022 ORDER BY last_name;

-- Courses with credits > 3, sorted descending
SELECT * FROM courses WHERE credits > 3 ORDER BY credits DESC;

-- Professors with salary between 80,000 and 95,000
SELECT * FROM professors WHERE salary BETWEEN 80000 AND 95000;

-- Students with email ending '@college.edu'
SELECT * FROM students WHERE email LIKE '%@college.edu';

-- Count students per enrollment_year
SELECT enrollment_year, COUNT(*) AS total_students
FROM students
GROUP BY enrollment_year;


-- Task 3: Multi-Table Joins


-- Student full name + department
SELECT CONCAT(s.first_name, ' ', s.last_name) AS full_name, d.dept_name
FROM students s
JOIN departments d ON s.department_id = d.department_id;

-- Enrollment with student name + course name
SELECT e.enrollment_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name, c.course_name
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id;

-- Students NOT enrolled in any course
SELECT s.student_id, s.first_name, s.last_name
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.student_id
WHERE e.course_id IS NULL;

-- Courses with number of students enrolled (include zero)
SELECT c.course_name, COUNT(e.student_id) AS total_enrolled
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_name;

-- Departments with professors + salaries (include empty depts)
SELECT d.dept_name, p.prof_name, p.salary
FROM departments d
LEFT JOIN professors p ON d.department_id = p.department_id;


-- Task 4: Aggregations & Grouping


-- Total enrollments per course
SELECT c.course_name, COUNT(e.enrollment_id) AS enrollment_count
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_name;

-- Average professor salary per department (rounded)
SELECT d.dept_name, ROUND(AVG(p.salary), 2) AS avg_salary
FROM departments d
JOIN professors p ON d.department_id = p.department_id
GROUP BY d.dept_name;

-- Departments with budget > 600,000
SELECT dept_name, budget FROM departments WHERE budget > 600000;

-- Grade distribution for CS101
SELECT grade, COUNT(*) AS grade_count
FROM enrollments e
JOIN courses c ON e.course_id = c.course_id
WHERE c.course_code = 'CS101'
GROUP BY grade;

-- Departments with >2 students enrolled
SELECT d.dept_name, COUNT(s.student_id) AS total_students
FROM departments d
JOIN students s ON d.department_id = s.department_id
GROUP BY d.dept_name
HAVING COUNT(s.student_id) > 2;
