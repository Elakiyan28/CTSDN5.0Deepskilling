USE college_db;


-- Task 1: Subqueries


--  Students enrolled in more courses than the average
SELECT s.student_id, s.first_name, s.last_name
FROM students s
WHERE (SELECT COUNT(*) FROM enrollments e WHERE e.student_id = s.student_id) >
      (SELECT AVG(course_count) FROM (
          SELECT COUNT(*) AS course_count
          FROM enrollments
          GROUP BY student_id
      ) AS sub);

--  Courses where all enrolled students got 'A'
SELECT c.course_name
FROM courses c
WHERE NOT EXISTS (
    SELECT 1 FROM enrollments e
    WHERE e.course_id = c.course_id AND e.grade <> 'A'
);

--  Professor with highest salary in each department
SELECT p.prof_name, p.salary, d.dept_name
FROM professors p
WHERE p.salary = (
    SELECT MAX(p2.salary) FROM professors p2
    WHERE p2.department_id = p.department_id
);

--  Departments with avg salary > 85,000
SELECT dept_name, avg_salary
FROM (
    SELECT d.dept_name, AVG(p.salary) AS avg_salary
    FROM departments d
    JOIN professors p ON d.department_id = p.department_id
    GROUP BY d.dept_name
) AS sub
WHERE avg_salary > 85000;


-- Task 2: Views


--  Student enrollment summary view
CREATE OR REPLACE VIEW vw_student_enrollment_summary AS
SELECT s.student_id,
       CONCAT(s.first_name, ' ', s.last_name) AS full_name,
       d.dept_name,
       COUNT(e.course_id) AS total_courses,
       AVG(CASE e.grade
            WHEN 'A' THEN 4 WHEN 'B' THEN 3
            WHEN 'C' THEN 2 WHEN 'D' THEN 1
            WHEN 'F' THEN 0 END) AS gpa
FROM students s
JOIN departments d ON s.department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, d.dept_name;

--  Course stats view
CREATE OR REPLACE VIEW vw_course_stats AS
SELECT c.course_name, c.course_code,
       COUNT(e.enrollment_id) AS total_enrollments,
       AVG(CASE e.grade
            WHEN 'A' THEN 4 WHEN 'B' THEN 3
            WHEN 'C' THEN 2 WHEN 'D' THEN 1
            WHEN 'F' THEN 0 END) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id;

--  Query students with GPA > 3.0
SELECT * FROM vw_student_enrollment_summary WHERE gpa > 3.0;

--  Attempt UPDATE through multi-table view (will fail)
-- UPDATE vw_student_enrollment_summary SET dept_name='Test' WHERE student_id=1;

--  Drop views and recreate with CHECK OPTION
DROP VIEW vw_student_enrollment_summary;
DROP VIEW vw_course_stats;

CREATE VIEW vw_student_enrollment_summary AS
SELECT student_id, first_name, last_name, enrollment_year
FROM students
WHERE enrollment_year = 2022
WITH CHECK OPTION;


-- Task 3: Stored Procedures & Transactions


--  Procedure to enroll student
DELIMITER //
CREATE PROCEDURE sp_enroll_student(IN sid INT, IN cid INT, IN edate DATE)
BEGIN
    IF EXISTS (SELECT 1 FROM enrollments WHERE student_id = sid AND course_id = cid) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Duplicate enrollment not allowed';
    ELSE
        INSERT INTO enrollments(student_id, course_id, enrollment_date) VALUES (sid, cid, edate);
    END IF;
END //
DELIMITER ;

--  Procedure to transfer student department with transaction
CREATE TABLE department_transfer_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    old_dept INT,
    new_dept INT,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE PROCEDURE sp_transfer_student(IN sid INT, IN newDept INT)
BEGIN
    DECLARE oldDept INT;
    START TRANSACTION;
    SELECT department_id INTO oldDept FROM students WHERE student_id = sid;
    UPDATE students SET department_id = newDept WHERE student_id = sid;
    INSERT INTO department_transfer_log(student_id, old_dept, new_dept)
    VALUES (sid, oldDept, newDept);
    COMMIT;
END //
DELIMITER ;

-- Test rollback by inserting invalid dept_id
-- CALL sp_transfer_student(1, 999); -- should rollback

--  SAVEPOINT example
START TRANSACTION;
INSERT INTO enrollments(student_id, course_id, enrollment_date, grade)
VALUES (1, 2, '2022-07-01', 'A');
SAVEPOINT sp1;
-- Next insert fails deliberately
INSERT INTO enrollments(student_id, course_id, enrollment_date, grade)
VALUES (1, 999, '2022-07-01', 'B');
ROLLBACK TO sp1;
COMMIT;
