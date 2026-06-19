USE college_db;

-- Task 1: Trigger - Log Student Insertions


CREATE TABLE student_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    action VARCHAR(50),
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE TRIGGER after_student_insert
AFTER INSERT ON students
FOR EACH ROW
BEGIN
    INSERT INTO student_log (student_id, action)
    VALUES (NEW.student_id, 'INSERT');
END //
DELIMITER ;

-- Test trigger
INSERT INTO students (first_name, last_name, email, date_of_birth, department_id, enrollment_year)
VALUES ('TriggerTest', 'X', 'triggertest@example.com', '2005-07-01', 1, 2023);

SELECT * FROM student_log;

-- =========================
-- Task 2: Trigger - Prevent Negative Salary
-- =========================

DELIMITER //
CREATE TRIGGER check_professor_salary
BEFORE INSERT ON professors
FOR EACH ROW
BEGIN
    IF NEW.salary < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Salary cannot be negative';
    END IF;
END //
DELIMITER ;

-- Test trigger (should fail)
INSERT INTO professors (prof_name, email, department_id, salary)
VALUES ('InvalidProf', 'invalid@example.com', 1, -50000);

-- Task 3: Performance Tuning - Indexes


-- Create index on enrollments for faster lookups
CREATE INDEX idx_enrollment_student_course ON enrollments(student_id, course_id);

-- Test performance improvement
SELECT s.first_name, c.course_name, e.grade
FROM enrollments e
INNER JOIN students s ON e.student_id = s.student_id
INNER JOIN courses c ON e.course_id = c.course_id
WHERE e.student_id = 1;


-- Task 4: Performance Tuning - EXPLAIN


EXPLAIN
SELECT s.first_name, c.course_name, e.grade
FROM enrollments e
INNER JOIN students s ON e.student_id = s.student_id
INNER JOIN courses c ON e.course_id = c.course_id
WHERE e.student_id = 1;
